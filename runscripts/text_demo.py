import time

import matplotlib
import matplotlib.pyplot as plt


from mplkit.window import Window
from mplkit.horizontal_box import HorizontalBox as HBox
from mplkit.vertical_box import VerticalBox as VBox
from mplkit.label import Label
from mplkit.line_edit import LineEdit
from mplkit.combo_box import ComboBox
from mplkit.spacer import Spacer


def main():


    l1 = Label(3, 0.5, 'Top label')

    le1 = LineEdit(3, 0.5, 'EditMe!')

    l2 = Label(3, 0.5, 'Bottom label')

    le2 = LineEdit(3, 0.5, 'abcdef0123456789')

    sp1 = Spacer(3,0.25)

    cb = ComboBox(3, 0.5, ['one', 'two', 'three'])

    sp2 = Spacer(3, 3)

    vbox = VBox()

    vbox.append(l1, le1, l2, le2, sp1, cb, sp2)

    w = Window(vbox, 'Text Demo')

    plt.show()


if __name__ == "__main__":
    main()