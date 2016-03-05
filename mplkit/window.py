
import matplotlib as mpl
import matplotlib.pyplot as plt


class Window(object):
    """
    A window in which to add widgets.
    """

    def __init__(self, box, title = 'Window', padding = 0.10, toolbar = False):
        """
        width & height in inches
        """

        self._box = box
        self._padding = padding

        w, h = box.size()

        padding = 0.10

        w += 2.0 * padding
        h += 2.0 * padding

        orig_toolbar_settig = mpl.rcParams['toolbar']

        if not toolbar:
            mpl.rcParams['toolbar'] = 'None'

        self._fig = plt.figure(figsize=(w,h))

        self._fig.canvas.set_window_title(title)

        x = padding
        y = padding

        box._render(self._fig, x, y)

        # restore default rcparams
        mpl.rcParams['toolbar'] = orig_toolbar_settig
