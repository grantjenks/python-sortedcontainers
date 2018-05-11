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
    from blist import sortedset
    kinds['B-Tree'] = sortedset
except ImportError:
    warnings.warn('No module named blist', ImportWarning)

try:
    from banyan import SortedSet as BanyanSortedSet
    kinds['RB-Tree'] = BanyanSortedSet
except ImportError:
    warnings.warn('No module named banyan', ImportWarning)

try:
    from skiplistcollections import SkipListSet
    kinds['Skip-List'] = SkipListSet
except ImportError:
    warnings.warn('No module named skiplistcollections', ImportWarning)

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

limit('add', 'B-Tree', 10000)

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

limit('update_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update',
        'limit': 1000000
    }

limit('update_large', 'B-Tree', 10000)

remove('update_tiny', 'Skip-List')
remove('update_small', 'Skip-List')
remove('update_medium', 'Skip-List')
remove('update_large', 'Skip-List')

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

limit('union_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['union_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union',
        'limit': 1000000
    }

limit('union_large', 'B-Tree', 10000)

remove('union_tiny', 'Skip-List')
remove('union_small', 'Skip-List')
remove('union_medium', 'Skip-List')
remove('union_large', 'Skip-List')

for name, kind in kinds.items():
    impls['remove'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'remove',
        'limit': 1000000
    }

limit('remove', 'B-Tree', 10000)

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

for name, kind in kinds.items():
    impls['difference_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference',
        'limit': 1000000
    }

limit('difference_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['difference_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference',
        'limit': 1000000
    }

limit('difference_large', 'B-Tree', 10000)

remove('difference_tiny', 'Skip-List')
remove('difference_small', 'Skip-List')
remove('difference_medium', 'Skip-List')
remove('difference_large', 'Skip-List')

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

limit('difference_update_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['difference_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update',
        'limit': 1000000
    }

limit('difference_update_large', 'B-Tree', 10000)

remove('difference_update_tiny', 'Skip-List')
remove('difference_update_small', 'Skip-List')
remove('difference_update_medium', 'Skip-List')
remove('difference_update_large', 'Skip-List')

for name, kind in kinds.items():
    impls['intersection_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_tiny', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['intersection_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_small', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['intersection_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['intersection_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection',
        'limit': 1000000
    }

limit('intersection_large', 'B-Tree', 10000)

remove('intersection_tiny', 'Skip-List')
remove('intersection_small', 'Skip-List')
remove('intersection_medium', 'Skip-List')
remove('intersection_large', 'Skip-List')

for name, kind in kinds.items():
    impls['intersection_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_tiny', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['intersection_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_small', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['intersection_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['intersection_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update',
        'limit': 1000000
    }

limit('intersection_update_large', 'B-Tree', 10000)

remove('intersection_update_tiny', 'Skip-List')
remove('intersection_update_small', 'Skip-List')
remove('intersection_update_medium', 'Skip-List')
remove('intersection_update_large', 'Skip-List')

for name, kind in kinds.items():
    impls['symmetric_difference_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_tiny', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_small', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference',
        'limit': 1000000
    }

limit('symmetric_difference_large', 'B-Tree', 10000)

remove('symmetric_difference_tiny', 'Skip-List')
remove('symmetric_difference_small', 'Skip-List')
remove('symmetric_difference_medium', 'Skip-List')
remove('symmetric_difference_large', 'Skip-List')

for name, kind in kinds.items():
    impls['symmetric_difference_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_tiny', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_small', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_medium', 'B-Tree', 10000)

for name, kind in kinds.items():
    impls['symmetric_difference_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update',
        'limit': 1000000
    }

limit('symmetric_difference_update_large', 'B-Tree', 10000)

remove('symmetric_difference_update_tiny', 'Skip-List')
remove('symmetric_difference_update_small', 'Skip-List')
remove('symmetric_difference_update_medium', 'Skip-List')
remove('symmetric_difference_update_large', 'Skip-List')

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

remove('init', 'Skip-List')
limit('init', 'B-Tree', 100000)

if __name__ == '__main__':
    main('SortedSet')
