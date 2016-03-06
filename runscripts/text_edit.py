import time

import matplotlib
import matplotlib.pyplot as plt


from mplkit.window import Window
from mplkit.horizontal_box import HorizontalBox as HBox
from mplkit.vertical_box import VerticalBox as VBox
from mplkit.label import Label
from mplkit.line_edit import LineEdit


def main():


    l1 = Label(3, 0.5, 'Top label')

    le = LineEdit(3, 0.5, 'EditMe!')

    l2 = Label(3, 0.5, 'Bottom label')

    vbox = VBox()

    vbox.append(l1, le, l2)

    w = Window(vbox, 'LineEdit Demo')

    plt.show()


if __name__ == "__main__":
    main()