"""
Benchmark Sorted Set Datatypes
"""

import warnings
from sys import hexversion

from .benchmark import *

if hexversion < 0x03000000:
    range = xrange

# Tests.

@register_test
def contains(func, size):
    for val in lists[size][::100]:
        assert func(val)

@register_test
def iter(func, size):
    assert all(idx == val for idx, val in enumerate(func()))

@register_test
def add(func, size):
    for val in lists[size][::100]:
        func(-val)

@register_test
def update_tiny(func, size):
    func(range(size, size + 10))

@register_test
def update_small(func, size):
    func(range(size, size + int(size / 10)))

@register_test
def update_medium(func, size):
    func(range(size, size + int(size * 5 / 10)))

@register_test
def update_large(func, size):
    func(range(size, size + int(size * 9 / 10)))

@register_test
def union_tiny(func, size):
    func(range(size, size + 10))

@register_test
def union_small(func, size):
    func(range(size, size + int(size / 10)))

@register_test
def union_medium(func, size):
    func(range(size, size + int(size * 5 / 10)))

@register_test
def union_large(func, size):
    func(range(size, size + int(size * 9 / 10)))

@register_test
def remove(func, size):
    for val in lists[size][::100]:
        func(val)

@register_test
def difference_tiny(func, size):
    func(range(int(size / 2), int(size / 2) + 10))

@register_test
def difference_small(func, size):
    func(range(int(size / 2), int(size / 2) + int(size / 10)))

@register_test
def difference_medium(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 5 / 10)))

@register_test
def difference_large(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 9 / 10)))

@register_test
def difference_update_tiny(func, size):
    func(range(int(size / 2), int(size / 2) + 10))

@register_test
def difference_update_small(func, size):
    func(range(int(size / 2), int(size / 2) + int(size / 10)))

@register_test
def difference_update_medium(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 5 / 10)))

@register_test
def difference_update_large(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 9 / 10)))

@register_test
def intersection_tiny(func, size):
    func(range(int(size / 2), int(size / 2) + 10))

@register_test
def intersection_small(func, size):
    func(range(int(size / 2), int(size / 2) + int(size / 10)))

@register_test
def intersection_medium(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 5 / 10)))

@register_test
def intersection_large(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 9 / 10)))

@register_test
def intersection_update_tiny(func, size):
    func(range(int(size / 2), int(size / 2) + 10))

@register_test
def intersection_update_small(func, size):
    func(range(int(size / 2), int(size / 2) + int(size / 10)))

@register_test
def intersection_update_medium(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 5 / 10)))

@register_test
def intersection_update_large(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 9 / 10)))

@register_test
def symmetric_difference_tiny(func, size):
    func(range(int(size / 2), int(size / 2) + 10))

@register_test
def symmetric_difference_small(func, size):
    func(range(int(size / 2), int(size / 2) + int(size / 10)))

@register_test
def symmetric_difference_medium(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 5 / 10)))

@register_test
def symmetric_difference_large(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 9 / 10)))

@register_test
def symmetric_difference_update_tiny(func, size):
    func(range(int(size / 2), int(size / 2) + 10))

@register_test
def symmetric_difference_update_small(func, size):
    func(range(int(size / 2), int(size / 2) + int(size / 10)))

@register_test
def symmetric_difference_update_medium(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 5 / 10)))

@register_test
def symmetric_difference_update_large(func, size):
    func(range(int(size / 2), int(size / 2) + int(size * 9 / 10)))

@register_test
def pop(func, size):
    for rpt in range(int(size / 100)):
        func()

@register_test
def init(func, size):
    func(lists[size])

# Setups.

def do_nothing(obj, size):
    pass

def fill_values(obj, size):
    if hasattr(obj, 'update'):
        obj.update(sorted(lists[size]))
    else:
        for val in lists[size]:
            obj.add(val)

# Implementation imports.

from .context import sortedcontainers
from sortedcontainers import SortedSet
kinds['SortedSet'] = SortedSet

try:
    from rbtree import rbset
    kinds['rbset'] = rbset
except ImportError:
    warnings.warn('No module named rbtree', ImportWarning)

try:
    from blist import sortedset
    kinds['blist.sortedset'] = sortedset
except ImportError:
    warnings.warn('No module named blist', ImportWarning)

try:
    from skiplistcollections import SkipListSet
    kinds['SkipListSet'] = SkipListSet
except ImportError:
    warnings.warn('No module named skiplistcollections', ImportWarning)

try:
    from banyan import SortedSet as BanyanSortedSet
    kinds['banyan.SortedSet'] = BanyanSortedSet
except ImportError:
    warnings.warn('No module named banyan', ImportWarning)

# Implementation configuration.

from .benchmark import remove

for name in tests:
    impls[name] = OrderedDict()

for name, kind in kinds.items():
    impls['contains'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__contains__',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['iter'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__iter__',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['add'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'add',
        'limit': 1000000
    }

limit('add', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update',
        'limit': 1000000
    }

limit('update_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update',
        'limit': 1000000
    }

limit('update_large', 'blist.sortedset', 10000)

remove('update_tiny', 'SkipListSet')
remove('update_small', 'SkipListSet')
remove('update_medium', 'SkipListSet')
remove('update_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['union_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['union_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['union_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union',
        'limit': 1000000
    }

limit('union_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['union_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union',
        'limit': 1000000
    }

limit('union_large', 'blist.sortedset', 10000)

remove('union_tiny', 'SkipListSet')
remove('union_small', 'SkipListSet')
remove('union_medium', 'SkipListSet')
remove('union_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['remove'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'remove',
        'limit': 1000000
    }

limit('remove', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['difference_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['difference_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference',
        'limit': 1000000
    }

limit('difference_small', 'rbset', 10000)

for name, kind in kinds.items():
    impls['difference_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference',
        'limit': 1000000
    }

limit('difference_medium', 'rbset', 10000)
limit('difference_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['difference_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference',
        'limit': 1000000
    }

limit('difference_large', 'rbset', 10000)
limit('difference_large', 'blist.sortedset', 10000)

remove('difference_tiny', 'SkipListSet')
remove('difference_small', 'SkipListSet')
remove('difference_medium', 'SkipListSet')
remove('difference_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['difference_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['difference_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['difference_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update',
        'limit': 1000000
    }

limit('difference_update_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['difference_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update',
        'limit': 1000000
    }

limit('difference_update_large', 'blist.sortedset', 10000)

remove('difference_update_tiny', 'SkipListSet')
remove('difference_update_small', 'SkipListSet')
remove('difference_update_medium', 'SkipListSet')
remove('difference_update_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['intersection_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_tiny', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['intersection_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_small', 'rbset', 10000)
limit('intersection_small', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['intersection_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_medium', 'rbset', 10000)
limit('intersection_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['intersection_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_large', 'rbset', 10000)
limit('intersection_large', 'blist.sortedset', 10000)

remove('intersection_tiny', 'SkipListSet')
remove('intersection_small', 'SkipListSet')
remove('intersection_medium', 'SkipListSet')
remove('intersection_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['intersection_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_tiny', 'rbset', 10000)
limit('intersection_update_tiny', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['intersection_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_small', 'rbset', 10000)
limit('intersection_update_small', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['intersection_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_medium', 'rbset', 10000)
limit('intersection_update_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['intersection_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_large', 'rbset', 10000)
limit('intersection_update_large', 'blist.sortedset', 10000)

remove('intersection_update_tiny', 'SkipListSet')
remove('intersection_update_small', 'SkipListSet')
remove('intersection_update_medium', 'SkipListSet')
remove('intersection_update_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['symmetric_difference_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_tiny', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_small', 'rbset', 10000)
limit('symmetric_difference_small', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_medium', 'rbset', 10000)
limit('symmetric_difference_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_large', 'rbset', 10000)
limit('symmetric_difference_large', 'blist.sortedset', 10000)

remove('symmetric_difference_tiny', 'SkipListSet')
remove('symmetric_difference_small', 'SkipListSet')
remove('symmetric_difference_medium', 'SkipListSet')
remove('symmetric_difference_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['symmetric_difference_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_tiny', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_small', 'rbset', 10000)
limit('symmetric_difference_update_small', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_medium', 'rbset', 10000)
limit('symmetric_difference_update_medium', 'blist.sortedset', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_large', 'rbset', 10000)
limit('symmetric_difference_update_large', 'blist.sortedset', 10000)

remove('symmetric_difference_update_tiny', 'rbset')
remove('symmetric_difference_update_small', 'rbset')
remove('symmetric_difference_update_medium', 'rbset')
remove('symmetric_difference_update_large', 'rbset')
remove('symmetric_difference_update_tiny', 'SkipListSet')
remove('symmetric_difference_update_small', 'SkipListSet')
remove('symmetric_difference_update_medium', 'SkipListSet')
remove('symmetric_difference_update_large', 'SkipListSet')

for name, kind in kinds.items():
    impls['pop'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'pop',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['init'][name] = {
        'setup': do_nothing,
        'ctor': kind,
        'func': 'update',
        'limit': 1000000
    }

remove('init', 'SkipListSet')

limit('init', 'blist.sortedset', 100000)

if __name__ == '__main__':
    main('SortedSet')
