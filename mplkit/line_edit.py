import numpy as np
from matplotlib import rcParams

from mplkit.label import Label


class LineEdit(Label):
    """
    A text label.
    """

    IDLE = 0
    TYPING = 1

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
        pad_left = 0.025 # inches

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

        self._kwargs = kwargs

        self._pad_left = pad_left

        if notify and not iscallable(notify):
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
            'key_press_event', self._on_key_down)


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

        self._axes.figure.canvas.draw()


    def _start_typing(self, x_pixel):

        self._mode = self.TYPING
        self._render_cursor(x_pixel, 'pixel')
        self._orig_text = self.text()


    def _stop_typing(self, notify = True):

        notify = False

        if self._mode == self.TYPING:
            """
            Reactive standandard keymap
            """

            for key in self._rc_keys_disable:
                rcParams[key] = self._rc_keys_disable[key]

            notify = True

        self._mode = self.IDLE
        self._cursor.set_visible(False)
        self._axes.figure.canvas.draw()

        if notify and self._notify:
            self._notify(self.text())


    def _on_mouse_down(self, event):

        # FIXME: add enable/disable flags

        if event.inaxes != self._axes:
            self._stop_typing()
            return

#~        if event.canvas.mouse_grabber != self._axes:
#~            event.canvas.grab_mouse(self._axes)

        if self._mode == self.IDLE:

            # disable the default keymap

            self._rc_keys_disable = {}

            for key in self._rc_keys_to_disable:
                self._rc_keys_disable[key] = rcParams[key]
                rcParams[key] = []

        self._start_typing(event.x)


    def _on_key_down(self, event):

        # FIXME: ignore if disabled

        if self._mode != self.TYPING:
            return

        key = event.key

#~        print "key = ", repr(key)

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

            N = len(self.text())

            if self._cursor_idx >= N:
                return

            s = self.text()

            s = s[0:self._cursor_idx] + s[self._cursor_idx+1:]

            self.text(s)

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'left':

            if self._cursor_idx == 0:
                return

            self._cursor_idx -= 1

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'right':

            N = len(self.text())

            if self._cursor_idx == N:
                return

            self._cursor_idx += 1

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'home':

            if self._cursor_idx == 0:
                return

            self._cursor_idx = 0

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'end':

            N = len(self.text())

            if self._cursor_idx == N:
                return

            self._cursor_idx = N

            self._render_cursor(self._cursor_idx, 'index')

        elif key == 'enter':
            self._stop_typing()

        elif key == 'escape':
            self._stop_typing()
            self.text(self._orig_text)

        else:
            print "unhandled = ", repr(key)



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
