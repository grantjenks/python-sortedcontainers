"""Plot histogram of SortedList sublist lengths while items are added.

Script output is a video named `sublist-lengths.mp4`. The video displays a line
graph where the x-axis is sublist length and the y-axis is the percentage of
sublists with that length. Sublist lengths are divided into buckets as with a
histogram. A line fitting the histogram as a normal distribution is plotted
alongside in green.

A line graph was used to represent the histogram because it was easier to
animate.

Observations:

* Average sublist length cycles between `load` and `load * 2` with an
  exponentially increasing period.

* As the number of elements increases, the sublist length distribution can be
  approximated by a normal distribution. The fit is valid within 30% of the
  mean.

* At the end of the video, the normal distribution fitting the histogram with
  mean=1500 has standard deviation=102.94.

* Observing the mean and standard deviation over time shows that the standard
  deviation tends to increase at a given mean over time. In this way, the curve
  flattens as more values are added to it.

"""

from __future__ import division, print_function

import argparse
import itertools as it
import numpy as np
import scipy
import scipy.stats
import sortedcontainers as sc
from matplotlib import pyplot as plt
from matplotlib import animation
import random

DISPLAY_FIT = False

def background():
    "Plot the background of each animated frame."
    hist_line.set_data([], [])
    norm_line.set_data([], [])
    return hist_line, norm_line


def frame(num):
    "Draw frame."
    values.update(func() for func in it.repeat(random.random, LOAD))
    data = np.array([len(sublist) for sublist in values._lists])
    hist, bins = np.histogram(data, bins=BINS, normed=True)
    hist_line.set_data(bins[:-1], hist)
    norm = scipy.stats.norm
    params = norm.fit(data)
    norm_line.set_data(LENGTHS, norm.pdf(LENGTHS, *params))

    if DISPLAY_FIT:
        print('Normal', '%10.3f %10.3f' % params)

    return hist_line, norm_line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--load', type=float, default=1e3)
    parser.add_argument('--show', action='store_true')
    parser.add_argument('--filename', default='sublist-lengths-add.mp4')
    parser.add_argument('--display-fit', action='store_true')

    args = parser.parse_args()

    random.seed(args.seed)

    LOAD = int(args.load)
    BINS = np.array(range(LOAD, LOAD * 2 + 1, LOAD // 20))
    LENGTHS = np.array(range(LOAD, LOAD * 2))
    DISPLAY_FIT = args.display_fit

    values = sc.SortedList(load=LOAD)

    # Initialize with random values.

    for func in it.repeat(random.random, LOAD):
        values.add(func())

    fig = plt.figure()
    bounds = (LOAD - 5 * LOAD // 100, LOAD * 2 - 5 * LOAD // 100)
    ax = plt.axes(xlim=bounds, ylim=(0, 0.01))
    hist_line, = ax.plot([], [])
    norm_line, = ax.plot([], [])

    animator = animation.FuncAnimation(
        fig, frame, init_func=background, frames=1000, interval=10, blit=True,
    )

    if args.show:
        plt.show()
    else:
        animator.save(
            args.filename, fps=20, extra_args=['-vcodec', 'libx264']
        )
