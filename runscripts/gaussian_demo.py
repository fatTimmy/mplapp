import argparse


import numpy as np
import matplotlib
import matplotlib.pyplot as plt


from mplkit.window import Window
from mplkit.horizontal_box import HorizontalBox as HBox
from mplkit.vertical_box import VerticalBox as VBox
from mplkit.label import Label
from mplkit.spacer import Spacer
from mplkit.button import Button
from mplkit.slider import Slider
from mplkit.plot import Plot


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d',
        '--debug',
        action = 'store_true',
        help = 'Show the bounding boxes around Spacers and Labels.'
    )

    args = parser.parse_args()

    if args.debug:
        Debug.value = True

    #--------------------------------------------------------------------------
    # various sizes of widget element

    title_height = 1.5

    plot_height = 6
    plot_width = 7

    plot_left   = 1.0
    plot_bottom = 0.75

    mu_height = 0.5

    slider_size = 0.25

    fontsize = 28

    # default values

    mu = 0.0
    sigma = 1.0

    # limits

    mu0 = -5.0
    mu1 = 5.0

    sigma0 = 0.0
    sigma1 = 5.0

    #--------------------------------------------------------------------------
    # create some widgets that will be the targets of callbacks

    mu_value_label = Label(0.50, slider_size, ' %.2f' % mu, ha = 'left', ec = get_edgecolor())
    sigma_value_label = Label(0.50, plot_height, ' %.2f' % sigma, ha = 'left', ec = get_edgecolor())
    plot = Plot(plot_width, plot_height)

    # objects that respond to the sliders and redraw the plot

    gaussian_drawer = DrawGaussian(plot)

    mu_updater = LabelUpdater('mu', mu_value_label, gaussian_drawer.redraw)
    sigma_updater = LabelUpdater('sigma', sigma_value_label, gaussian_drawer.redraw)

    #--------------------------------------------------------------------------
    # column 1: spacer title, spacer plot left, spacer plot bottom, mu label

    col1 = VBox(padding = 0.05)

    # space on the of the title
    sp = make_spacer(plot_left, title_height)

    col1.append(sp)

    # space on the left of the plot

    sp = make_spacer(plot_left, plot_height)

    col1.append(sp)

    # plot bottom spacer

    sp = make_spacer(plot_left, plot_bottom)

    col1.append(sp)

    # mu label ont he left of the mu slider

    label = Label(
        plot_left,
        slider_size,
        '$\mu$  ',
        ha = 'right',
        fontsize = fontsize,
        ec = get_edgecolor(),
    )

    col1.append(label)

    #--------------------------------------------------------------------------
    # column 2: title, plot, plot bottom spacer, mu slider

    col2 = VBox(padding = 0.05)

    # title

    title = Label(
        plot_width,
        title_height,
        ('The Gaussian function: ' r'$e^{-\frac{(t-\mu)^2}{2\sigma^2}}$'),
        fontsize = fontsize,
        ec = get_edgecolor(),
    )

    col2.append(title)

    # plot widget

    col2.append(plot)

    # plot bottom spacer

    sp = make_spacer(plot_width, plot_bottom)

    col2.append(sp)

    # mu slider

    slider = Slider(
        plot_width,
        slider_size,
        notify = mu_updater.update,
        vmin = mu0,
        vmax = mu1,
        vinit = mu,
    )

    col2.append(slider)

    #--------------------------------------------------------------------------
    # column 3: spacer title, sigma slider, plot bottom spacer, mu value label

    col3 = VBox(padding = 0.05)

    sp = make_spacer(0.1, title_height)

    col3.append(sp)

    # sigma slider: a horizontal box with sigma label, slider, value label

    label = Label(
        0.50,
        plot_height,
        '$ \sigma$',
        ec = get_edgecolor(),
        fontsize = fontsize,
    )

    slider = Slider(
        slider_size,
        plot_height,
        notify = sigma_updater.update,
        vmin = sigma0,
        vmax = sigma1,
        vinit = sigma,
    )

    hbox = HBox(padding = 0.05)

    hbox.append(label, slider, sigma_value_label)

    col3.append(hbox)

    # mu value label, plus spacer

    sp = make_spacer(0.1, plot_bottom)

    col3.append(sp, mu_value_label, 'left')

    # one more spacer to padd the window's bottom edge

    sp = make_spacer(0.1, 0.25)

    col3.append(sp)

    #--------------------------------------------------------------------------
    # render the window and make draw initial gaussian curve

    hbox = HBox(va = 'top', padding = 0.05)

    hbox.append(col1, col2, col3)

    window = Window(hbox, 'Gaussian Drawing')

    # all widgets are now rendered, plot on the Plot widget

    plt.sca(plot.axes())

    # construct time axis

    samplerate = 100

    x = np.linspace(mu0, mu1, (mu1 - mu0) * samplerate)

    y = gaussian_drawer.compute(x, mu, sigma)

    plt.plot(x, y, 'b-')
    plt.grid(True)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.xlim([mu0, mu1])
    plt.ylim([-0.05, 1.05])

    # enter matplotlib event loop

    plt.show()


#------------------------------------------------------------------------------
# support utilities

class Debug(object):
    value = False


class Count(object):
    value = 0


def make_spacer(w, h):

    if Debug.value:

        widget = Label(
            w,
            h,
            'sp%d' % Count.value,
            ec = get_edgecolor(),
            ha = 'left',
            va = 'top',
        )

    else:

        widget = Spacer(w, h)

    Count.value += 1

    return widget


def get_edgecolor():

    if Debug.value:
        return 'k'

    else:
        return 'none'


class LabelUpdater(object):

    def __init__(self, name, label, notify, fmt = ' %.2f'):

        self._name = name
        self._label = label
        self._fmt = fmt
        self._notify = notify


    def update(self, new_value):
        self._label.text(self._fmt % new_value)
        self._notify(name = self._name, value = new_value)


class DrawGaussian(object):

    def __init__(self, plot_widget):

        self._plot_widget = plot_widget

        self._line = None
        self._time_axis = None


    def compute(self, taxis, mu, sigma):
        """
        Computes the new y data.
        """
        return np.exp(- ( (taxis - mu) ** 2 / (2 * sigma ** 2)))


    def redraw(self, name = '', value = None):

        if self._line is None:

            self._line = self._plot_widget.axes().get_lines()[0]

            self._time_axis = self._line.get_data()[0]

        mu = 0.0
        sigma = 1.0

        if name == 'mu':
            mu = value

        elif name == 'sigma':
            sigma = value

        x = self._time_axis

        y = self.compute(x, mu, sigma)

        self._line.set_data(x, y)
        self._line.axes.figure.canvas.draw_idle()


if __name__ == "__main__":
    main()