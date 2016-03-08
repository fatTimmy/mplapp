import numpy as np

from matplotlib import rcParams
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

import pyperclip


from mplkit.line_edit import LineEdit


class ComboBox(LineEdit):
    """
    A ComboxBox, upon clicking button, drops down a list of items to choose.

    Items can be edited also.
    """

    def __init__(
            self,
            width,
            height,
            text_list,
            edit_notify = None,
            selection_notify = None,
            **kwargs
        ):

        if len(text_list) > 0:
            text = text_list[0]
        else:
            text = ''

        super(ComboBox,self).__init__(
            width, height, text, edit_notify, **kwargs)

        #---------------------------------------------------------------------
        # additional items
        #
        # selection axes for showing the possible selections
        # a rectangle to highlight the selection row
        # a button to show the selection drop down

        self._select_axes = None
        self._select_highlight = None # just a rectangle
        self._select_button = None    # Just a rectangle


    def _render(self, fig, x, y):

        super(ComboBox, self)._render(fig, x, y)

        self._render_dropdown_button(fig)
        self._render_dropdown_axis(fig, x, y)


    def _render_dropdown_axis(self, fig, x, y):

        W, H = fig.get_size_inches()

        h = 10 * self._height

        y -= h

        x /= W
        y /= H

        # create the other gui assets but keep them hidden

        # selection axes, same width, by 10 times in height

        w = self._width / W
        h /= H

        ax = fig.add_axes([x, y, w, h], xticks=[], yticks=[])

        ax.set_xlim([0, self._width])
        ax.set_ylim([0, 10 * self._height])

        ax.set_axis_bgcolor('white')

        ax.set_visible(False)

        ax.set_zorder(1000)

        self._select_axes = ax


    def _render_dropdown_button(self, fig):

        w, h = 0.25, self._height * 0.25

        hw = w / 2.0
        hh = h / 2.0

        x = self._width - w - 0.02
        y = (self._height - h) / 2.0

        # Three point polygon:
        #
        #  2 O-----O 3
        #     \   /
        #      \ /
        #       O
        #       1
        #

        points = [
            [ x + hw, y    ],
            [ x,      y + h],
            [ x + w,  y + h],
        ]

        points = np.array(points)

        patch = Polygon(points, closed = True, ec = 'black', fc = 'black')

        self._axes.add_patch(patch)

        self._select_button = patch






