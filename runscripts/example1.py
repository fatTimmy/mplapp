import time

import matplotlib
import matplotlib.pyplot as plt


from mplkit.window import Window
from mplkit.horizontal_box import HorizontalBox as HBox
from mplkit.vertical_box import VerticalBox as VBox
from mplkit.label import Label
from mplkit.button import Button


def main():

    bw,bh = 1.5,1.5

    #--------------------------------------------------------------------------
    # window 1

    has = ['left', 'center', 'right']
    vas = ['top', 'center', 'bottom']

    vbox = VBox()

    for ha in has:

        labels = []

        for va in vas:
            labels.append(Label(bw,bh, 'Hello!', ha = ha, va = va, ec = 'w'))

        hb = HBox()
        hb.append(*labels)

        vbox.append(hb)

    w = Window(vbox, '3x3 label boxes')

    #--------------------------------------------------------------------------
    # window 2

    class MyButtonListener(object):

        def __init__(self, **kwargs):
            self._button = Button(bw,bh, 'ClickMe (0)', self._on_click, **kwargs)
            self._count = 0

        def button(self):
            return self._button

        def _on_click(self, _):

            self._count += 1

            if self._count % 5 == 0:
                self._button.text('Disabled')
                self._button.disable()
            else:
                self._button.text('ClickMe (%d)' % self._count)


    class ButtonEnabler(object):

        def __init__(self, target_buttons, **kwargs):

            if not isinstance(target_buttons, list):
                target_buttons = [target_buttons]

            self._targets = target_buttons
            self._button = Button(bw,bh, 'Enable', self._on_click, **kwargs)


        def button(self):
            return self._button


        def _on_click(self, _):

            for b in self._targets:
                b.text('ClickMe')
                b.enable()


    l1 = Label(bw,bh, 'Label Left')

    b1 = MyButtonListener()
    b2 = ButtonEnabler(b1.button())

    l2 = Label(bw,bh, 'Label Right')

    hbox = HBox()

    hbox.append(l1, b1.button(), b2.button(), l2)

    w = Window(hbox, 'HBox Buttons')

    #--------------------------------------------------------------------------
    # window 3

    l1 = Label(bw,bh, 'Label Top')

    b1 = MyButtonListener(fc = 'blue', ec = 'red', color = 'white')
    b2 = ButtonEnabler(b1.button())

    l2 = Label(bw,bh, 'Label Bottom')

    vbox = VBox()

    vbox.append(l1, b1.button(), b2.button(), l2)

    w = Window(vbox, 'VBox Buttons')

    plt.show()


if __name__ == "__main__":
    main()