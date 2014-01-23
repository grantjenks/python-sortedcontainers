"""
Benchmark Sorted Set Datatypes
"""

from benchmark import *

# Tests.

@register_test
def contains(func, size):
    for val in lists[size]:
        assert func(val)

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

if __name__ == '__main__':
    main()
