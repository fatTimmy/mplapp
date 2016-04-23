import time

import matplotlib
import matplotlib.pyplot as plt


from mplapp.window import Window
from mplapp.horizontal_box import HorizontalBox as HBox
from mplapp.vertical_box import VerticalBox as VBox
from mplapp.label import Label
from mplapp.button import Button
from mplapp.slider import Slider


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


    l1 = Label(bw,1.0, 'Label Left\nva=top', ec = 'w')

    b1 = MyButtonListener()
    b2 = ButtonEnabler(b1.button())

    l2 = Label(bw, 1.0, 'Label Right\nva=bottom', ec = 'w')

    hbox = HBox()

    hbox.append(l1, 'top', b1.button(), b2.button(), l2, 'bottom')

    w = Window(hbox, 'HBox Buttons')

    #--------------------------------------------------------------------------
    # window 3

    l1 = Label(1.0,bh, 'Label Top\nha=left', ec = 'w')

    b1 = MyButtonListener(fc = 'blue', ec = 'red', color = 'white')
    b2 = ButtonEnabler(b1.button())

    l2 = Label(1.0,bh, 'Label Bottom\nha=right', ec = 'w')

    vbox = VBox()

    vbox.append(l1, 'left', b1.button(), b2.button(), l2, 'right')

    w = Window(vbox, 'VBox Buttons')

    #--------------------------------------------------------------------------
    # window 4

    class HSlider(object):

        def __init__(self):

            s = Slider(3, 0.25, notify = self._on_notify)

            self._label = Label(0.40, 0.25, '0.50')

            self._hbox = HBox()

            self._hbox.append(s, self._label)

        def hbox(self):
            return self._hbox

        def _on_notify(self, value):
            self._label.text('%.2f' % value)


    class VSlider(object):

        def __init__(self):

            s = Slider(0.25, 3.0, notify = self._on_notify)

            spacer = Label(0.40, 0.25, '') # keeps the slider centered

            self._label = Label(0.40, 0.25, '0.50')

            self._hbox = HBox()

            self._hbox.append(spacer, s, self._label)

        def hbox(self):
            return self._hbox

        def _on_notify(self, value):
            self._label.text('%.2f' % value)


    hs = HSlider()
    vs = VSlider()

    vbox = VBox()

    vbox.append(hs.hbox(), vs.hbox())

    w = Window(vbox, 'Sliders')

    plt.show()


if __name__ == "__main__":
    main()