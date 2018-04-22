"""Count splits that occur in SortedList._expand with varying loads.

NOTE: Benchmarking performance at scale eventually used sampling rather than
what is described below. Do not use this method for benchmarking. This file is
kept for SortedListWithSplits which presents an example for recording the
number of sublist splits that occur.

Compare three load styles:

1. Low - Simply initializing a SortedList creates each sublist with length
equal to `load`.

2. Normal Random - See `init_sorted_list` below. Each sublist is given a length
chosen at random from a normal distribution with mean 1500 and standard
deviation 100. See `plot_lengths_histogram.py` for a visualization of the
sublist length and motivation for the normal distribution parameters.

3. Added Random - Each sublist is initialized by simply adding random values to
the list. This one is the most realistic but expensive to compute. It's also
biased by the number of values added. Because SortedList amortizes some costs,
this metric is prone to under or over-estimating impact.

Sample output: LIMIT = int(1e6), RATIO = 1

Low [504, 490, 487, 503, 488, 494, 496, 502, 493, 486]
Normal Random [666, 667, 662, 666, 670, 668, 668, 666, 668, 666]
Added Random [685, 675, 689, 687, 699, 706, 691, 679, 672, 702]

Conclusion:

Normal Random is about 1-2% less than Added Random on average but remains
practical for use as an efficient approximation.

The above values were calculated with RATIO = 1. Increasing the ratio to 10
creates a significant divergence between Normal Random and Added Random. Sample
output with RATIO = 10:

Low [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Normal Random [1, 2, 0, 1, 0, 1, 0, 1, 1, 2]
Added Random [307, 286, 290, 253, 279, 319, 283, 264, 278, 280]

The difference is due to the load of the sublists. Randomly adding a million
values positions the sublist lengths in a bimodal distribution split at 1000
and 2000. This is nearly the worst-case scenario for measurements.

After trying a number of settings, RATIO = 3 appears reliable and useful. This
approximates the available capacity:

    >>> random.seed(0)
    >>> sl = init_sorted_list(sc.SortedList(), int(1e6))
    >>> len(sl._lists) * sl._load * 2 - len(sl)
    334000

So after constructing a SortedList with sublist length given by a normal
distribution with mean 1,500 and standard deviation 100, we fill the remaining
empty capacity.

"""

from __future__ import print_function

import sortedcontainers as sc
import random

REPEAT = 5
LIMIT = int(1e6)
RATIO = 3


class SortedListWithSplits(sc.SortedList):
    "SortedList that counts splits that occur in _expand."
    
    def __init__(self, *args, **kwargs):
        self.splits = 0
        super(SortedListWithSplits, self).__init__(*args, **kwargs)

    def _expand(self, pos):
        if len(self._lists[pos]) > self._twice:
            self.splits += 1
        super(SortedListWithSplits, self)._expand(pos)


def init_sorted_list(sl, size):
    "Initialize a SortedList with normally distributed sublist lengths."
    sl.clear()

    total = 0

    while total < size:
        # count = random.randrange(sl._load, sl._twice)
        count = int(random.normalvariate(int(sl._load * 1.5), 100))
        count = min(count, sl._load * 2)
        count = max(count, sl._load)
        sl._lists.append(list(range(total, total + count)))
        total += count

    sl._len = sum(len(sublist) for sublist in sl._lists)
    sl._maxes[:] = [sublist[-1] for sublist in sl._lists]

    sl._check()

    while len(sl) > size:
        del sl[random.randrange(len(sl))]

    return sl


def fill(obj, count, limit):
    "Repeatedly add random values to the SortedList."
    for each in range(count):
        obj.add(random.randrange(limit))


if __name__ == '__main__':
    low_splits = []

    for each in range(REPEAT):
        sl = SortedListWithSplits(range(LIMIT))
        fill(sl, LIMIT / RATIO, LIMIT)
        low_splits.append(sl.splits)

    uniform_splits = []

    for each in range(REPEAT):
        sl = init_sorted_list(SortedListWithSplits(), LIMIT)
        fill(sl, LIMIT / RATIO, LIMIT)
        uniform_splits.append(sl.splits)

    rand_splits = []

    for each in range(REPEAT):
        sl = SortedListWithSplits()

        values = list(range(LIMIT))
        random.shuffle(values)
        for value in values:
            sl.add(value)

        sl.splits = 0

        fill(sl, LIMIT / RATIO, LIMIT)
        rand_splits.append(sl.splits)

    print('Low', low_splits)
    print('Normal Random', uniform_splits)
    print('Added Random', rand_splits)
