
class VerticalBox(object):


    def __init__(self, padding = 0.05):
        self._widgets = []
        self._padding = padding


    def append(self, *widgets):
        self._widgets.extend(widgets)


    def size(self):
        """
        Returns the minimum size of this box in inches.
        """

        w = 0
        h = 0

        for g in self._widgets:
            tw, th = g.size()

            h += th + self._padding
            w = max(w, tw)

        h -= self._padding

        return w,h


    def _render(self, fig, x, y):

        for w in self._widgets:
            w._render(fig, x, y)

            y += w.size()[1] + self._padding
