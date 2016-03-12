
import matplotlib


class Plot(object):
    """
    A wrapper for an Axes.
    """

    def __init__(self, width, height, **kwargs):

        self._width = float(width)
        self._height = float(height)
        self._axes = None


    def axes(self):
        return self._axes


    def size(self):
        return (self._width, self._height)


    def _render(self, fig, x, y):

        # convert size to percent of figure

        W, H = fig.get_size_inches()

        x /= W
        y /= H

        w, h = self.size()

        w /= W
        h /= H

        self._axes = fig.add_axes([x, y, w, h])
