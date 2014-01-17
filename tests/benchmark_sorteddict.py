"""
Benchmark Sorted Dictionary Datatypes
"""

import time, random
from collections import defaultdict

random.seed(0)
sizes = [10, 100, 1000, 10000, 100000] # 1000000
lists = {key: list(xrange(key)) for key in sizes}
for key in sizes:
    random.shuffle(lists[key])

# Benchmarking.

def measure(test, func, size):
    start = time.clock()
    test(func, size)
    end = time.clock()
    return (end - start)

def benchmark(test, name, ctor, setup, func_name):
    for size in sizes:
        # warmup

        obj = ctor()
        setup(obj, size)
        func = getattr(obj, func_name)
        measure(test, func, size)
        
        # record

        times = []
        for rpt in xrange(5):
            obj = ctor()
            setup(obj, size)
            func = getattr(obj, func_name)
            times.append(measure(test, func, size))

        print test.func_name, name, size, min(times), max(times), times[2], sum(times) / len(times)

# Tests

def getitem(func, size):
    for val in lists[size]:
        assert func(val) == -val

def setitem(func, size):
    for val in lists[size]:
        func(val, -val)

def delitem():
    pass

# Setups

def do_nothing(obj, size):
    pass

def fill_values(obj, size):
    for val in lists[size]:
        obj[val] = -val

# Implementations

impls = defaultdict(dict)

from context import sortedcontainers
from sortedcontainers import SortedDict

from rbtree import rbtree
from blist import sorteddict

# todo

from treap import treap
from bintrees import FastAVLTree, FastRBTree
from skiplistcollections import SkipListDict

impls[getitem]['sortedcontainers.SortedDict'] = {
    'setup': fill_values,
    'ctor': SortedDict,
    'func': '__getitem__'
}

impls[getitem]['rbtree.rbtree'] = {
    'setup': fill_values,
    'ctor': rbtree,
    'func': '__getitem__'
}

impls[getitem]['blist.sorteddict'] = {
    'setup': fill_values,
    'ctor': sorteddict,
    'func': '__getitem__'
}

impls[setitem]['sortedcontainers.SortedDict'] = {
    'setup': do_nothing,
    'ctor': SortedDict,
    'func': '__setitem__'
}

impls[setitem]['rbtree.rbtree'] = {
    'setup': do_nothing,
    'ctor': rbtree,
    'func': '__setitem__'
}

impls[setitem]['blist.sorteddict'] = {
    'setup': do_nothing,
    'ctor': sorteddict,
    'func': '__setitem__'
}

if __name__ == '__main__':
    # Add switches
    # -testname
    # -datatypename

    for test in impls:
        for name in impls[test]:
            details = impls[test][name]
            benchmark(test, name, details['ctor'], details['setup'], details['func'])
