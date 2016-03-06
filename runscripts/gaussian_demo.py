import numpy as np
import matplotlib
import matplotlib.pyplot as plt


from mplkit.window import Window
from mplkit.horizontal_box import HorizontalBox as HBox
from mplkit.vertical_box import VerticalBox as VBox
from mplkit.label import Label
from mplkit.button import Button
from mplkit.slider import Slider
from mplkit.plot import Plot


def main():

    # plot is 6 x 4 inches

    # title label will be 7 x 1

    title = Label(6, 1.5,
        ('The Gaussian function: '
            r'$e^{-\frac{(t-\mu)^2}{2\sigma^2}}$'),
        fontsize = 28)

    g_draw = GaussianDrawer(6, 4, pad_left = 0.7, pad_bottom = 0.5)

    # sigma slider's total width should be 1 inch

    sigma_slider = MySlider(
        0.20, 0.25, 0.55,
        height = 3.5,
        text = r'$\sigma$',
        notify = g_draw.draw,
        vmin = 0.001,
        vmax = 5.0,
        vinit = 1.0
    )

    # mu slider is under the plot and sigma slider, 7 x 0.25

    mu_slider = MySlider(
        0.65, 5.35, 0.5,
        height = 0.25,
        text = r'$\mu$',
        notify = g_draw.draw,
        vmin = -5.0,
        vmax = 5.0,
        vinit = 0.0
    )

    #--------------------------------------------------------------------------
    # push everything into a set of horizontal and vertical boxes for alignmnt

    vbox = VBox()

    # row 1

    vbox.append(title)

    # row 2

    temp = HBox()

    # spacer
    spacer = Label(0.25, 0.25, '')

    temp.append(g_draw.widget(), spacer, sigma_slider.hbox(), 'top')

    vbox.append(temp)

    # row 3

    # adding a spacer

    spacer = Label(1, 0.10, '')

    vbox.append(spacer, mu_slider.hbox(), 'left')

    #--------------------------------------------------------------------------
    # render final window

    w = Window(vbox, 'Gaussian Drawing')

    # stimulate the first drawing
    g_draw.draw()

    plt.show()




class MySlider(object):


    def __init__(self, label_width, slider_width, value_width, height, notify, **kwargs):
        """
        Creates the slider for adjusting mu.
        """

        self._height = float(height)
        self._width = float(label_width + slider_width + value_width)
        self._notify = notify

        self._text = kwargs['text']

        mu_label = Label(label_width, height, self._text + ' ', ha = 'right', fontsize = 16)

        slider = Slider(
            slider_width,
            height,
            vmin = kwargs['vmin'],
            vmax = kwargs['vmax'],
            vinit = kwargs['vinit'],
            notify = self._update_value_label
        )

        tinit = ' %.3f' % kwargs['vinit']

        self._value_label = Label(value_width, height, tinit, ha = 'left')

        self._hbox = HBox()

        self._hbox.append(mu_label, slider, self._value_label)


    def _update_value_label(self, value):
        self._value_label.text(' %.3f' % value)
        self._notify(text = self._text, value = value)


    def hbox(self):
        return self._hbox


class GaussianDrawer(object):

    def __init__(self, width, height, sr = 100, tmin = -5.0, tmax = 5.0, **kwargs):

        self._sr = sr
        self._taxis = np.linspace(tmin, tmax, (tmax - tmin) * sr)

        self._plot = Plot(width, height, pad_top = 0.0, **kwargs)

        self._mu = 0.0
        self._sigma = 1.0

        self._line = None


    def widget(self):
        return self._plot


    def _draw(self, mu, sigma):
        """
        Computes the new y data.
        """

        t = np.array(self._taxis)

        return np.exp(- ( (t - mu) ** 2 / (2 * sigma ** 2)))


    def draw(self, **kwargs):

        text = kwargs.get('text', '')

        if 'mu' in text:
            self._mu = kwargs['value']

        elif 'sigma' in text:
            self._sigma = kwargs['value']

        axes = self._plot.axes()

        if axes == None:

            # not rendered yet

            return

        if self._line is None:
            # first time drawing on axes

            plt.sca(axes)

            self._line = plt.plot(
                self._taxis, self._draw(self._mu, self._sigma), 'b-')[0]

            plt.grid(True)
            plt.xlabel('Time (t)')
            plt.ylabel('Amplitude')
            plt.xlim([self._taxis[0]-0.5, self._taxis[-1] + 0.5])
            plt.ylim([-0.1, 1.1])

        else:

            # update the y data
            self._line.set_ydata(self._draw(self._mu, self._sigma))

        axes.figure.canvas.draw_idle()


if __name__ == "__main__":
    main()