"""Benchmark SortedContainers at scale.

## Local Results

$ pypy benchmark_scale.py --limit 1e9
@   Method    Size   Operations           Time       Ops/Sec     Ratio
@      add   1e+06        1e+04        0.01501    666045.025       nan
@      add   1e+07        1e+05        0.26612    375764.681     1.773
@      add   1e+08        1e+06        4.69080    213183.298     1.763
@      add   1e+09        1e+07       83.01831    120455.358     1.770
@      del   1e+06        1e+04        0.00827   1208897.485       nan
@      del   1e+07        1e+05        0.13309    751393.836     1.609
@      del   1e+08        1e+06        3.79143    263752.866     2.849
@      del   1e+09        1e+07      124.59184     80262.081     3.286

## High Memory Instance Results

Note: Requires ~128 GB of memory.
Note: Requires ~11 hrs to run.

$ nohup /home/grantj/PyPy27/bin/pypy benchmark_scale.py &
$ cat nohup.out
@   Method    Size     Ops           Time       Ops/Sec     Ratio
@      add   1e+06   1e+04        0.02133    468884.826       nan
@      add   1e+07   1e+05        0.38629    258872.924     1.811
@      add   1e+08   1e+06        6.20695    161109.825     1.607
@      add   1e+09   1e+07      120.24735     83161.919     1.937
@      add   1e+10   1e+08     2416.60713     41380.330     2.010
@      del   1e+06   1e+04        0.01791    558289.343       nan
@      del   1e+07   1e+05        0.26171    382097.449     1.461
@      del   1e+08   1e+06        6.11150    163626.036     2.335
@      del   1e+09   1e+07      171.58899     58278.798     2.808
@      del   1e+10   1e+08     5493.95076     18201.838     3.202

### CPU Info

Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                32
On-line CPU(s) list:   0-31
Thread(s) per core:    2
Core(s) per socket:    16
Socket(s):             1
NUMA node(s):          1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 63
Model name:            Intel(R) Xeon(R) CPU @ 2.30GHz
Stepping:              0
CPU MHz:               2299.998
BogoMIPS:              4599.99
Hypervisor vendor:     KVM
Virtualization type:   full
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              46080K
NUMA node0 CPU(s):     0-31

"""
from __future__ import print_function

import argparse
import collections as co
import functools as ft
import gc
import itertools as it
import math
import random
import sortedcontainers as sc
import sys
import time


CHECK = False


def iter_with_description(iterable, description=''):
    "Placeholder iterator function with ignored description parameter."
    return iter(iterable)


PROGRESS = iter_with_description


def init_sorted_list(sl, size, moment=5, fraction=0.1):
    """Initialize SortedList with normally distributed sublist lengths.

    The mean of the normal distribution is given by:

        mu = load * (1.0 + moment / 10.0)

    And the standard deviation of the normal distribution is given by:

        sigma = load * fraction

    For a visualization of positive and negative moments see:

        * plot_lengths_histogram.py
        * plot_lengths_histogram_delitem.py

    :param SortedList sl: SortedList to initialize
    :param int size: size of the resulting SortedList
    :param int moment: number between -5 and 9 inclusive
    :param float fraction: fraction of load to be used as standard deviation
    :return: initialized sorted list

    """
    assert -5 <= moment <= 9
    assert 0 < fraction

    sl.clear()

    load = sl._load
    half = sl._load >> 1
    twice = sl._load << 1
    mu = load * (1.0 + moment / 10.0)
    sigma = load * fraction
    total = 0

    class WhileIterator(object):
        "Convert for-loop to while-loop with length estimate."
        def __iter__(self):
            while total < size:
                yield True
        def __len__(self):
            if moment < 0:
                return size / half
            else:
                return size / load

    for each in PROGRESS(WhileIterator(), 'init-sub'):
        count = int(random.normalvariate(mu, sigma))

        if moment >= 0:
            if count < load:
                count += load
            elif count > twice:
                count -= load

            count = min(count, twice)
            count = max(count, load)
        else:
            if count < half:
                count += half
            elif count > load:
                count -= half

            count = min(count, load)
            count = max(count, half)

        sl._lists.append(list(xrange(total, total + count)))
        total += count

    sl._len = sum(len(sublist) for sublist in sl._lists)
    sl._maxes[:] = [sublist[-1] for sublist in sl._lists]

    for each in PROGRESS(xrange(len(sl) - size), 'init-del'):
        del sl[random.randrange(len(sl))]

    del sl._index[:]

    if CHECK: sl._check()

    assert len(sl) == size

    return sl


def timeit(func):
    "Decorator to time function calls."
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        "Return timed duration of function call. Ignores function result."
        start = time.clock()
        result = func(*args, **kwargs)
        end = time.clock()
        return (end - start)
    return wrapper


@timeit
def add(obj, numbers):
    "Repeatedly add number from numbers to sorted list."
    for number in PROGRESS(numbers, 'add'):
        obj.add(number)


@timeit
def delitem(obj, indices):
    "Repeatedly delete values from sorted list by index in indices."
    for index in PROGRESS(indices, 'del'):
        del obj[index]


def randvalues(limit, fraction=0.001):
    "Return fraction of limit random values between 0 and limit."
    iterable = PROGRESS(xrange(int(limit * fraction)), 'randvalues')
    return [random.randrange(limit) for each in iterable]


def randindices(limit, fraction=0.002):
    "Return fraction of limit random indices counting down from limit."
    stop = limit - int(limit * fraction)
    iterable = PROGRESS(xrange(limit, stop, -1), 'randindices')
    return [random.randrange(length) for length in iterable]


def benchmark_add(start, limit, times):
    """Benchmark sorted list add method.

    Start and limit are an inclusive range of magnitudes.

    The load of the sorted list is the cube root of the size.

    Measurements are made by sampling performance at each "moment" of a sorted
    list while items are added to it. See `init_sorted_list` for how "moment"
    is used.

    """
    for exponent in xrange(start, limit + 1):
        timings = []
        count = 10 ** exponent
        sl = sc.SortedList(load=int(count ** (1.0 / 3)))

        for attempt in xrange(times):
            subtimings = []

            for moment in xrange(10):
                values = randvalues(count)
                init_sorted_list(sl, count, moment)
                gc.collect()
                subtiming = add(sl, values)
                subtimings.append(subtiming)

            timing = sum(subtimings)
            timings.append(timing)

        display('add', timings, count)


def benchmark_del(start, limit, times):
    """Benchmark sorted list delitem method.

    Start and limit are an inclusive range of magnitudes.

    The load of the sorted list is the square root of the size.

    Measurements are made by sampling performance at each "moment" of a sorted
    list while items are deleted from it. See `init_sorted_list` for how
    "moment" is used.

    """
    for exponent in xrange(start, limit + 1):
        timings = []
        count = 10 ** exponent
        sl = sc.SortedList(load=int(count ** (1.0 / 3))) # 2)))

        for attempt in xrange(times):
            subtimings = []

            for moment in xrange(-5, 0):
                indices = randindices(count)
                init_sorted_list(sl, count, moment)
                gc.collect()
                subtiming = delitem(sl, indices)
                subtimings.append(subtiming)

            timing = sum(subtimings)
            timings.append(timing)

        display('del', timings, count)


def display(name, times, size, last=['', 0]):
    "Display performance summary with ratio of ops/sec."

    times.sort()
    median_time = times[len(times) / 2]
    operations = size / 100
    ops_sec = operations / median_time

    last_name, last_ops_sec = last
    ratio = last_ops_sec / ops_sec if name == last_name else float('nan')
    last[0], last[1] = name, ops_sec

    template = '@%9s   %.0e   %.0e %14.5f  %12.3f    %6.3f'
    print(template % (name, size, operations, median_time, ops_sec, ratio))
    sys.stdout.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', default=1e6, type=float)
    parser.add_argument('--limit', default=1e10, type=float)
    parser.add_argument('--seed', default=0, type=int)
    parser.add_argument('--times', default=5, type=int)
    parser.add_argument('--funcs', default='all', choices=['all', 'add', 'del'])
    parser.add_argument('--progress', action='store_true')
    parser.add_argument('--check', action='store_true')

    args = parser.parse_args()

    random.seed(args.seed)

    if args.progress:
        import tqdm
        PROGRESS = tqdm.tqdm

    CHECK = args.check

    start = int(math.log10(args.start))
    limit = int(math.log10(args.limit))

    template = '@%9s %7s %7s %14s  %12s %9s'
    header = 'Method', 'Size', 'Ops', 'Time', 'Ops/Sec', 'Ratio'
    print(template % header)
    sys.stdout.flush()

    if args.funcs == 'all':
        benchmarks = [benchmark_add, benchmark_del]
    elif args.funcs == 'add':
        benchmarks = [benchmark_add]
    elif args.funcs == 'del':
        benchmarks = [benchmark_del]
    else:
        raise ValueError(args.funcs)

    for benchmark in benchmarks:
        benchmark(start, limit, args.times)
