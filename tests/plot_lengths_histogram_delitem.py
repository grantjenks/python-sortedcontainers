"""Plot histogram of SortedList sublist lengths while items are deleted.

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


def background():
    "Plot the background of each animated frame."
    hist_line.set_data([], [])
    norm_line.set_data([], [])
    return hist_line, norm_line


def frame(num):
    "Draw frame."
    for value in xrange(LOAD):
        del values[random.randrange(len(values))]
    data = np.array([len(sublist) for sublist in values._lists])
    hist, bins = np.histogram(data, bins=BINS) # , normed=True)
    hist_line.set_data(bins[:-1], hist)

    return hist_line, norm_line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--load', type=float, default=1e3)
    parser.add_argument('--show', action='store_true')
    parser.add_argument('--filename', default='sublist-lengths-delitem.mp4')

    args = parser.parse_args()

    random.seed(args.seed)

    LOAD = int(args.load)
    BINS = np.array(range(LOAD // 2, LOAD * 2 + 1, LOAD // 20))

    values = sc.SortedList(xrange(LOAD * LOAD), load=LOAD)

    fig = plt.figure()
    bounds = (LOAD // 2 - 5 * LOAD // 100, LOAD * 2 - 5 * LOAD // 100)
    ax = plt.axes(xlim=bounds, ylim=(0, 1000))
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
