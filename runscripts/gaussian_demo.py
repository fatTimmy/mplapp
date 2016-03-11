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

    # total width shall be 10 inches

    W = 10

    plot_width = 7
    plot_height = 5.0
    plot_bottom = 0.4
    left_padding = 1.0

    title = Label(plot_width, 1.5,
        ('The Gaussian function: '
            r'$e^{-\frac{(t-\mu)^2}{2\sigma^2}}$'),
        fontsize = 28,
        ec = 'k'
    )

    # left edge of plot padding

    g_draw = GaussianDrawer(
        plot_width,
        plot_height,
        pad_bottom = 0.5,
    )

    # sigma slider: is a vertical slider on the right of the plot

    label_width = 0.50
    value_width = 0.50
    slider_width = 0.25
    slider_height = plot_height - plot_bottom

    sigma_slider = MySlider(
        label_width,
        slider_width,
        value_width,
        height = plot_height,
        text = r'$\sigma$',
        notify = g_draw.draw,
        vmin = 0.001,
        vmax = 5.0,
        vinit = 1.0
    )

    # mu slider is under the plot

    label_width = left_padding

    mu_slider = MySlider(
        label_width,
        plot_width,
        value_width,
        height = 0.25,
        text = r'$\mu$',
        notify = g_draw.draw,
        vmin = -5.0,
        vmax = 5.0,
        vinit = 0.0
    )

    #--------------------------------------------------------------------------
    # push everything into a set of horizontal and vertical boxes for alignmnt

    ec = 'k'

    pad_left0 = Label(left_padding, 1.5, 'pad', ec = ec)
    pad_left1 = Label(left_padding, plot_height, 'pad', ec = ec, va = 'top')
    pad_right = Label(0.10, plot_height, '', ec = ec)
    plot_bottom = Label(left_padding, 0.5, 'pad', ec = ec)
    pad_bottom = Label(left_padding + plot_width, 0.10, '', ec = ec)

    vbox = VBox()

    # row 1

    hbox = HBox(padding = 0.0)

    hbox.append(pad_left0, title)

    vbox.append(hbox, 'left')

    # row 2

    hbox = HBox(padding = 0.0)

    hbox.append(pad_left1, g_draw.widget(), sigma_slider.hbox(), 'top', pad_right)

    vbox.append(hbox, plot_bottom, 'left')

    # row 3

    vbox.append(mu_slider.hbox(), 'left', pad_bottom, 'left')

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

        mu_label = Label(
            label_width,
            height,
            self._text + ' ',
            ha = 'right',
            fontsize = 28,
            ec = 'k'
        )

        slider = Slider(
            slider_width,
            height,
            vmin = kwargs['vmin'],
            vmax = kwargs['vmax'],
            vinit = kwargs['vinit'],
            notify = self._update_value_label
        )

        tinit = ' %.3f' % kwargs['vinit']

        self._value_label = Label(
            value_width,
            height,
            tinit,
            ha = 'left',
            ec = 'k'
        )

        self._hbox = HBox(padding = 0.0)

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

        self._plot = Plot(
            width,
            height,
            pad_top = 0.0,
            **kwargs
        )

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
            plt.xlim([self._taxis[0], self._taxis[-1]])
            plt.ylim([-0.1, 1.1])

        else:

            # update the y data
            self._line.set_ydata(self._draw(self._mu, self._sigma))

        axes.figure.canvas.draw_idle()


if __name__ == "__main__":
    main()