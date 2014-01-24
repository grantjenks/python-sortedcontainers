"""
Benchmark Sorted Set Datatypes
"""

from benchmark import *

# Tests.

@register_test
def contains(func, size):
    for val in lists[size]:
        assert func(val)

@register_test
def iter(func, size):
    count = 0
    for val in func():
        assert val == count
        count += 1

@register_test
def add(func, size):
    for val in lists[size]:
        func(val)

# Setups.

def do_nothing(obj, size):
    pass

def fill_values(obj, size):
    for val in lists[size]:
        obj.add(val)

# Implementation imports.

from context import sortedcontainers
from sortedcontainers import SortedSet
from rbtree import rbset
from blist import sortedset
from skiplistcollections import SkipListSet

kinds['SortedSet'] = SortedSet
kinds['rbset'] = rbset
kinds['sortedset'] = sortedset
kinds['SkipListSet'] = SkipListSet

# Implementation configuration.

for name in tests:
    impls[name] = OrderedDict()

for name, kind in kinds.items():
    impls['contains'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__contains__'
    }

for name, kind in kinds.items():
    impls['iter'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__iter__'
    }

for name, kind in kinds.items():
    impls['add'][name] = {
        'setup': do_nothing,
        'ctor': kind,
        'func': 'add'
    }

if __name__ == '__main__':
    main()
