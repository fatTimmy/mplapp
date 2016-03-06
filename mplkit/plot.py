
import matplotlib


class Plot(object):
    """
    A wrapper for an Axes.
    """

    def __init__(self, width, height, **kwargs):

        self._width = float(width)
        self._height = float(height)

        self._pad_left = kwargs.get('pad_left', 0.5)
        self._pad_right = kwargs.get('pad_right', 0.0)
        self._pad_top = kwargs.get('pad_top', 0.25)
        self._pad_bottom = kwargs.get('pad_bottom', 0.25)

        self._axes = None


    def axes(self):
        return self._axes


    def size(self):
        return (self._width, self._height)


    def _render(self, fig, x, y):

        # convert size to percent of figure

        W, H = fig.get_size_inches()

        x += self._pad_left
        y += self._pad_bottom

        x /= W
        y /= H

        w, h = self.size()

        w -= self._pad_left + self._pad_right
        h -= self._pad_top + self._pad_bottom

        w /= W
        h /= H

        self._axes = fig.add_axes([x, y, w, h])
