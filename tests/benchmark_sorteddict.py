"""
Benchmark Sorted Dictionary Datatypes
"""

import time, random, argparse
from collections import defaultdict, OrderedDict

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

tests = OrderedDict()

def register_test(func):
    tests[func.func_name] = func
    return func

# Tests

@register_test
def getitem(func, size):
    for val in lists[size]:
        assert func(val) == -val

@register_test
def setitem(func, size):
    for val in lists[size]:
        func(val, -val)

@register_test
def setitem_existing(func, size):
    for val in lists[size]:
        func(val, -val)

@register_test
def delitem(func, size):
    for val in lists[size]:
        func(val)

@register_test
def iter(func, size):
    count = 0
    for val in func():
        assert val == count
        count += 1

# Setups

def do_nothing(obj, size):
    pass

def fill_values(obj, size):
    for val in lists[size]:
        obj[val] = -val

# Implementation imports.

from context import sortedcontainers
from sortedcontainers import SortedDict
from rbtree import rbtree
from blist import sorteddict
from treap import treap
from bintrees import FastAVLTree, FastRBTree
from skiplistcollections import SkipListDict

kinds = OrderedDict()

kinds['SortedDict'] = SortedDict
kinds['rbtree'] = rbtree
kinds['sorteddict'] = sorteddict
kinds['treap'] = treap
kinds['FastAVLTree'] = FastAVLTree
kinds['FastRBTree'] = FastRBTree
kinds['SkipListDict'] = SkipListDict

# Implementations

impls = OrderedDict()

for name in tests:
    impls[name] = OrderedDict()

for name, kind in kinds.items():
    impls['getitem'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__getitem__'
    }

for name, kind in kinds.items():
    impls['setitem'][name] = {
        'setup': do_nothing,
        'ctor': kind,
        'func': '__setitem__'
    }

for name, kind in kinds.items():
    impls['setitem_existing'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__setitem__'
    }

for name, kind in kinds.items():
    impls['delitem'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__delitem__'
    }

for name, kind in kinds.items():
    impls['iter'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__iter__'
    }

# Setup

parser = argparse.ArgumentParser(description='Benchmark Sorted Dict Implementations')
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--test', action='append')
parser.add_argument('--kind', action='append')
parser.add_argument('--size', type=int, action='append')

args = parser.parse_args()

print 'Seed:', args.seed
random.seed(args.seed)

sizes = args.size or [10, 100, 1000, 10000, 100000]

print 'Sizes:', sizes

lists = {key: list(xrange(key)) for key in sizes}
for key in sizes:
    random.shuffle(lists[key])

# Script

if __name__ == '__main__':
    test_names = args.test or tests.keys()
    kind_names = args.kind or kinds.keys()

    print 'Tests:', test_names
    print 'Kinds:', kind_names

    print 'test_name', 'data_type', 'size', 'min', 'max', 'median', 'mean'

    for test in impls:
        if test not in test_names:
            continue
        for name in impls[test]:
            if name not in kind_names:
                continue
            details = impls[test][name]
            benchmark(tests[test], name, details['ctor'], details['setup'], details['func'])
