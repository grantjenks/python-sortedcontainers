"""
Benchmark Sorted Dictionary Datatypes
"""

from benchmark import *

# Tests.

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

# Setups.

def do_nothing(obj, size):
    pass

def fill_values(obj, size):
    for val in lists[size]:
        obj[val] = -val

# Implementation imports.

from .context import sortedcontainers
from sortedcontainers import SortedDict
from rbtree import rbtree
from blist import sorteddict
from treap import treap
from bintrees import FastAVLTree, FastRBTree
from skiplistcollections import SkipListDict

kinds['SortedDict'] = SortedDict
kinds['rbtree'] = rbtree
kinds['blist.sorteddict'] = sorteddict
kinds['treap'] = treap
kinds['FastAVLTree'] = FastAVLTree
kinds['FastRBTree'] = FastRBTree
kinds['SkipListDict'] = SkipListDict

# Implementation configuration.

for name in tests:
    impls[name] = OrderedDict()

for name, kind in kinds.items():
    impls['getitem'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__getitem__',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['setitem'][name] = {
        'setup': do_nothing,
        'ctor': kind,
        'func': '__setitem__',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['setitem_existing'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__setitem__',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['delitem'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__delitem__',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['iter'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__iter__',
        'limit': 100000
    }

if __name__ == '__main__':
    main('SortedDict')
