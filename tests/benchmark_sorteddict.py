"""
Benchmark Sorted Dictionary Datatypes
"""

import warnings
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
kinds['SortedDict'] = SortedDict

try:
    from rbtree import rbtree
    kinds['rbtree'] = rbtree
except ImportError:
    warnings.warn('No module named rbtree', ImportWarning)

try:
    from blist import sorteddict
    kinds['blist.sorteddict'] = sorteddict
except ImportError:
    warnings.warn('No module named blist', ImportWarning)

try:
    from treap import treap
    kinds['treap'] = treap
except ImportError:
    warnings.warn('No module named treap', ImportWarning)

try:
    from bintrees import FastAVLTree, FastRBTree
    kinds['FastAVLTree'] = FastAVLTree
    kinds['FastRBTree'] = FastRBTree
except ImportError:
    warnings.warn('No module named bintrees', ImportWarning)

try:
    from skiplistcollections import SkipListDict
    kinds['SkipListDict'] = SkipListDict
except ImportError:
    warnings.warn('No module named skiplistcollections', ImportWarning)

try:
    from banyan import SortedDict as BanyanSortedDict
    kinds['banyan.SortedDict'] = BanyanSortedDict
except ImportError:
    warnings.warn('No module named banyan', ImportWarning)

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
