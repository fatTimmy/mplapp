import numpy as np

from matplotlib import rcParams
from matplotlib.patches import Rectangle

import pyperclip


from mplkit.label import Label


class LineEdit(Label):
    """
    A text label.
    """

    IDLE = 0
    TYPING = 1
    SELECTING = 2

    def __init__(self, width, height, text, notify = None, **kwargs):

        self._str = text
        self._width = float(width)
        self._height = float(height)

        self._mode = self.IDLE

        # defaults
        ec = 'black'
        fc = 'white'
        color = 'black'
        ha = 'left'
        pad_left = 0.07 # inches
        highlight = [0.5859, 0.6406, 1.0]

        if 'ec' not in kwargs and 'edgecolor' not in kwargs:
            kwargs['ec'] = ec

        if 'fc' not in kwargs and 'facecolor' not in kwargs:
            kwargs['fc'] = fc

        if 'color' not in kwargs:
            kwargs['color'] = color

        if 'ha' not in kwargs and 'horizontalalignment' not in kwargs:
            kwargs['ha'] = ha

        if 'pad_left' in kwargs:
            pad_left = kwargs['pad_left']
            del kwargs['pad_left']

        if 'hl' in kwargs:
            highlight = kwargs['hl']
            del kwargs['hl']

        if 'highlight' in kwargs:
            highlight = kwargs['highlight']
            del kwargs['highlight']

        self._hl_color = highlight

        self._kwargs = kwargs

        self._pad_left = pad_left

        if notify and not callable(notify):
            raise ValueError('notify must be a callable function')

        self._notify = notify

        self._axes = None
        self._colors = ()

        # Capture keymap to be disabled

        self._rc_keys_to_disable = []

        for key in rcParams.keys():
            if u'keymap' in key:
                self._rc_keys_to_disable.append(key)

        self._cursor = None
        self._orig_text = None
        self._highlight = None


    def size(self):
        return (self._width, self._height)


    def text(self, new_text = None):

        if self._text is None:
            raise RuntimeError('This LineEdit ("%s") has been rendered yet')

        if new_text is None:
            return self._text.get_text()

        else:
            self._text.set_text(new_text)
            self._axes.figure.canvas.draw()


    def _render(self, fig, x, y):

        super(LineEdit, self)._render(fig, x, y)

        pos = list(self._text.get_position())

        pos[0] += self._pad_left

        self._text.set_position(pos)

        self._axes.figure.canvas.mpl_connect(
            'button_press_event', self._on_mouse_down)

        self._axes.figure.canvas.mpl_connect(
            'key_press_event', self._on_key_press)

        self._axes.figure.canvas.mpl_connect(
            'key_release_event', self._on_key_release)


    def _render_cursor(self, x, units):
        """
        Determine where to place cursor
        """

        # render subtext elements to find nearest charactor position for
        # the cursor

        text_idx, xdata = _search_text(self._text, x, units)

        self._cursor_idx = text_idx

        # first time rending cursor?
        if self._cursor is None:

            color = self._text.get_color()
            self._cursor = self._axes.axvline(xdata, 0.1, 0.9, color = color)

        else:
            self._cursor.set_data([[xdata, xdata], [0.1, 0.9]])

        self._cursor.set_visible(True)

        if self._mode == self.SELECTING:

            width = xdata - self._hl_x0
            self._highlight.set_width(width)


        self._axes.figure.canvas.draw()


    def _start_typing(self, x_pixel):

        self._mode = self.TYPING
        self._render_cursor(x_pixel, 'pixel')

        if self._orig_text is None:
            self._orig_text = str(self.text())


    def _stop_typing(self, key):

        self._mode = self.IDLE
        self._cursor.set_visible(False)
        self._axes.figure.canvas.draw()

        if self._notify and key == 'enter':
            self._notify(self.text())

        for key in self._rc_keys_disable:
            rcParams[key] = self._rc_keys_disable[key]


    def _start_selecting(self):

        x, _ = self._cursor.get_data()
        self._mode = self.SELECTING
        self._hl_x0 = x[0]

        if self._highlight is None:

            pos = self._hl_x0, 0

            r = Rectangle(pos, 0, 1, ec = self._hl_color, fc = self._hl_color)

            self._highlight = r

            self._axes.add_patch(r)

        else:
            self._highlight.set_x(self._hl_x0)
            self._highlight.set_width(0)
            self._highlight.set_visible(True)

        self._axes.figure.canvas.draw()


    def _stop_selecting(self):

        self._mode = self.TYPING
        if self._highlight:
            self._highlight.set_visible(False)
            self._axes.figure.canvas.draw()


    def _on_mouse_down(self, event):

        # FIXME: add enable/disable flags

        if event.inaxes != self._axes:
            return

        if self._mode == self.IDLE:

            # disable the default keymap

            self._rc_keys_disable = {}

            for key in self._rc_keys_to_disable:
                self._rc_keys_disable[key] = rcParams[key]
                rcParams[key] = []

        if event.dblclick:

            self._cursor_idx = 0

            self._render_cursor(self._cursor_idx, 'index')

            self._start_selecting()

            self._cursor_idx = len(self.text())

            self._render_cursor(self._cursor_idx, 'index')

            self._mode = self.TYPING

        else:
            self._start_typing(event.x)



    def _on_key_press(self, event):

        # FIXME: ignore if disabled

        if self._mode == self.IDLE:
            return

        key = event.key

        # normal keys are length 1

        if len(key) == 1:

            text_idx, xdata = _search_text(
                self._text, self._cursor_idx, 'index')

            s = self.text()

            s = s[0:text_idx] + key + s[text_idx:]

            self.text(s)

            self._cursor_idx += 1

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'backspace':

            if self._cursor_idx == 0:
                return

            text_idx, xdata = _search_text(
                self._text, self._cursor_idx, 'index')

            s = self.text()

            s = s[0:text_idx-1] + s[text_idx:]

            self.text(s)

            self._cursor_idx -= 1

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'delete':

            self._do_delete()

        elif key == 'left':

            if self._mode != self.SELECTING:
                self._stop_selecting()

            if self._cursor_idx == 0:
                return

            self._cursor_idx -= 1

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'right':

            if self._mode != self.SELECTING:
                self._stop_selecting()

            N = len(self.text())

            if self._cursor_idx == N:
                return

            self._cursor_idx += 1

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'home':

            if self._mode != self.SELECTING:
                self._stop_selecting()

            if self._cursor_idx == 0:
                return

            self._cursor_idx = 0

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'end':

            if self._mode != self.SELECTING:
                self._stop_selecting()

            N = len(self.text())

            if self._cursor_idx == N:
                return

            self._cursor_idx = N

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'enter':
            self._stop_typing(key)

        elif key == 'escape':
            self._stop_selecting()
            self._stop_typing(key)
            self.text(self._orig_text)
            self._orig_text = None
            self._mode = self.IDLE

        elif key == 'shift':
            self._start_selecting()

        elif key in ['ctrl+c', 'ctrl+x']:

            start, end = self._highlight.get_window_extent().get_points()

            x0, x1 = start[0], end[0]

            i0, _ = _search_text(self._text, x0, 'pixel')
            i1, _ = _search_text(self._text, x1, 'pixel')

            delta = i1 - i0

            if delta == 0:
                return

            s = self.text()

            pyperclip.copy(s[i0:i1])

            if key == 'ctrl+x':
                self._do_delete()


        elif key == 'ctrl+v':

            temp = pyperclip.paste()

            i0, i1 = self._get_selected_range()

            s = str(self.text())

            s = s[0:i0] + temp + s[i1:]

            self.text(s)

            self._cursor_idx = i0 + len(temp)

            self._render_cursor(self._cursor_idx, 'index')

            self._stop_selecting()

        else:
#~            print "unhandled = ", repr(key)
            pass


    def _on_key_release(self, event):

        key = event.key

        if key in 'shift' and self._mode == self.SELECTING:
            self._mode = self.TYPING

    def _get_selected_range(self):

        if self._highlight and self._highlight.get_visible():

            start, end = self._highlight.get_window_extent().get_points()

            x0, x1 = start[0], end[0]

            i0, _ = _search_text(self._text, x0, 'pixel')
            i1, _ = _search_text(self._text, x1, 'pixel')

            return i0, i1

        else:
            return self._cursor_idx, self._cursor_idx


    def _do_delete(self):
        """
        called by pressing the delete key or ctrl+x
        """

        N = len(self.text())

        s = self.text()

        i0, i1 = self._get_selected_range()

        if self._cursor_idx > i0:
            self._cursor_idx = i0

        if i1 > i0:
            s = s[0:i0] + s[i1:]

        elif i0 == i1:
            s = s[0:i0] + s[i0+1:]

        else:
            s = s[0:i0] + s[i1:]

        if self._highlight:
            self._stop_selecting()

        self._render_cursor(self._cursor_idx, 'index')
        self.text(s)


#------------------------------------------------------------------------------
# render text element and inspect the bounding box

def _search_text(text, x, units):

    if units == 'pixel':
        return _search_text_pixel(text, x)

    elif units == 'index':
        return _search_text_index(text, x)

    else:
        raise ValueError('unknown units "%s"' % units)


def _search_text_pixel(text, x_pixel):

    orig = text.get_text()

    # the backend render ignores trailing spaces, so we'll replace them for our
    # measurements

    s = orig.replace(' ', ',')

    N = len(s)

    x_positions = []
    delta = np.zeros((N + 1), dtype = np.float32)

    for i in range(N+1):

        txt = s[0:i]

        text.set_text(txt)

        bb = text.get_window_extent()

        x_positions.append(bb)

        start, end = bb.get_points()

        x1 = end[0]

        dist = float(x1) - float(x_pixel)

        delta[i] = abs(dist)

    # restore text
    text.set_text(orig)

    idx = delta.argmin()

    bb = x_positions[idx]

    # now convert pixels to data units

    inv = text.axes.transData.inverted()
    bb = inv.transform(bb)

    start, end = bb

    xdata = end[0]

    return idx, xdata


def _search_text_index(text, x_idx):

    orig = text.get_text()

    # the backend render ignores trailing spaces, so we'll replace them for our
    # measurements

    s = orig.replace(' ', ',')

    N = len(s)

    if x_idx < 0:
        raise IndexError('x_idx < 0 (%d < 0)' % x_idx)

    if x_idx > N:
        raise IndexError('x_idx > N (%d > %d)' % (x_idx, N))

    x_positions = []

    for i in range(x_idx + 1):

        txt = s[0:i]

        text.set_text(txt)

        bb = text.get_window_extent()

        start, end = bb.get_points()

        x_positions.append(bb)

    # restore text
    text.set_text(orig)

    bb = x_positions[x_idx]

    # now convert pixels to data units

    inv = text.axes.transData.inverted()
    bb = inv.transform(bb)

    start, end = bb

    xdata = end[0]

    return x_idx, xdata
