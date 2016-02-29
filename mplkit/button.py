# Python
import colorsys
import time

from matplotlib.colors import ColorConverter

from mplkit.label import Label


class Button(Label):
    """
    A push button.
    """

    def __init__(self, width, height, text, callback = None, **kwargs):

        if callback and not callable(callback):
            raise ValueError("callback isn't callable!")

        self._callback = callback

        ec = 'black'

        if 'ec' not in kwargs and 'edgecolor' not in kwargs:
            kwargs['ec'] = ec

        super(Button, self).__init__(width, height, text, **kwargs)


    def size(self):
        return (self._width, self._height)


    def _render(self, fig, x, y):
        super(Button, self)._render(fig, x, y)

        self._axes.figure.canvas.mpl_connect(
            'button_press_event',
            self._blink_on_click
        )


    def _blink_on_click(self, event):
        """
        'blink' the axis color to give visual feedback the button has been
        pressed.

        Reference: http://stackoverflow.com/a/1165145/562106

        """

        if event.inaxes != self._axes:
            return

        orig_color = self._axes.get_axis_bgcolor()

        r,g,b = ColorConverter().to_rgb(orig_color)

        cmax = max([r,g,b])
        cmin = min([r,g,b])

        # gray?
        if abs(cmax - cmin) < 5:

            if cmax > 0.5:
                r,g,b = 0.10,0.10,0.10
            else:
                r,g,b = 0.90,0.90,0.90

        h,l,s = colorsys.rgb_to_hls(r,g,b)

        # invert hue
        h = 360.0 - h

        new_color = colorsys.hls_to_rgb(h,l,s)

        self._axes.set_axis_bgcolor(new_color)
        self._axes.figure.canvas.draw()

        time.sleep(0.05)

        self._axes.set_axis_bgcolor(orig_color)
        self._axes.figure.canvas.draw()

        if self._callback:
            self._callback(event)




