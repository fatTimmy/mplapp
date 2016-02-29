import matplotlib
import matplotlib.pyplot as plt


from mplkit.window import Window
from mplkit.horizontal_box import HorizontalBox as HBox
from mplkit.vertical_box import VerticalBox as VBox
from mplkit.label import Label
from mplkit.button import Button

def main():

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

    hbox = HBox()

    def on_click(event):
        print('on_click()!')

    button = Button(3,3, 'ClickMe', on_click)

    l1 = Label(3,3, 'Label Left')
    l2 = Label(3,3, 'Label Right')

    hbox.append(l1, button, l2)

    w = Window(hbox, 'Push Button Demo')

    plt.show()


if __name__ == "__main__":
    main()