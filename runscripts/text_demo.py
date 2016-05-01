import time

import matplotlib
import matplotlib.pyplot as plt


from mplapp.window import Window
from mplapp.horizontal_box import HorizontalBox as HBox
from mplapp.vertical_box import VerticalBox as VBox
from mplapp.label import Label
from mplapp.line_edit import LineEdit
from mplapp.combo_box import ComboBox
from mplapp.spacer import Spacer


def main():

    width = 6

    l1 = Label(width, 0.5, 'Top label')

    le1 = LineEdit(
        width,
        0.5,
        'Using shift+arrow will select text, ctrl+a works too!',
    )

    l2 = Label(width, 0.5, 'Bottom label')

    le2 = LineEdit(
        width,
        0.5,
        'Click+moving the mouse selects text, double click sleects all'
    )

    sp1 = Spacer(width, 0.25)

    def on_combo_selected(index, text):
        print("Combo box selection: %d, %s" % (index, text))

    cb = ComboBox(
        width, 0.5, ['one', 'two', 'three'],
        selection_notify = on_combo_selected
    )

    sp2 = Spacer(width, 3)

    vbox = VBox()

    vbox.append(l1, le1, l2, le2, sp1, cb, sp2)

#~    vbox.append(l1, le1)

    w = Window(vbox, 'Text Demo (Experimental Work In Progress!)')

    plt.show()


if __name__ == "__main__":
    main()