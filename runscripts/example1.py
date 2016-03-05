import matplotlib
import matplotlib.pyplot as plt


from mplkit.window import Window
from mplkit.horizontal_box import HorizontalBox as HBox
from mplkit.vertical_box import VerticalBox as VBox
from mplkit.label import Label
from mplkit.button import Button

def main():

    # window 1

    has = ['left', 'center', 'right']
    vas = ['top', 'center', 'bottom']

    vbox = VBox()

    for ha in has:

        labels = []

        for va in vas:
            labels.append(Label(2,2, '+', ha = ha, va = va, ec = 'w'))

        hb = HBox()
        hb.append(*labels)

        vbox.append(hb)

    w = Window(vbox, '3x3 label boxes')

    # window 2

    class MyButtonListener(object):

        def __init__(self):
            self._button = Button(3,3, 'ClickMe (0)', self.on_click)
            self._count = 0

        def button(self):
            return self._button

        def on_click(self, event):
            self._count += 1
            self._button.text('ClickMe (%d)' % self._count)


    l1 = Label(3,3, 'Label Left')

    bl = MyButtonListener()

    l2 = Label(3,3, 'Label Right')

    hbox = HBox()

    hbox.append(l1, bl.button(), l2)

    w = Window(hbox, 'Push Button Demo')

    plt.show()


if __name__ == "__main__":
    main()