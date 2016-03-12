
class Spacer(object):
    """
    Just something that takes up space, to aid widget alignment.
    """

    def __init__(self, width, height):

        self._width = float(width)
        self._height = float(height)


    def size(self):
        return (self._width, self._height)


    def _render(self, fig, x, y):
        pass