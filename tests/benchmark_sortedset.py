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

@register_test
def update_tiny(func, size):
    func(xrange(size, size + 10))

@register_test
def update_small(func, size):
    func(xrange(size, size + size / 10))

@register_test
def update_medium(func, size):
    func(xrange(size, size + size * 5 / 10))

@register_test
def update_large(func, size):
    func(xrange(size, size + size * 9 / 10))

@register_test
def union_tiny(func, size):
    func(xrange(size, size + 10))

@register_test
def union_small(func, size):
    func(xrange(size, size + size / 10))

@register_test
def union_medium(func, size):
    func(xrange(size, size + size * 5 / 10))

@register_test
def union_large(func, size):
    func(xrange(size, size + size * 9 / 10))

@register_test
def remove(func, size):
    for val in lists[size]:
        func(val)

@register_test
def difference_tiny(func, size):
    func(xrange(size / 2, size / 2 + 10))

@register_test
def difference_small(func, size):
    func(xrange(size / 2, size / 2 + size / 10))

@register_test
def difference_medium(func, size):
    func(xrange(size / 2, size / 2 + size * 5 / 10))

@register_test
def difference_large(func, size):
    func(xrange(size / 2, size / 2 + size * 9 / 10))

@register_test
def difference_update_tiny(func, size):
    func(xrange(size / 2, size / 2 + 10))

@register_test
def difference_update_small(func, size):
    func(xrange(size / 2, size / 2 + size / 10))

@register_test
def difference_update_medium(func, size):
    func(xrange(size / 2, size / 2 + size * 5 / 10))

@register_test
def difference_update_large(func, size):
    func(xrange(size / 2, size / 2 + size * 9 / 10))

@register_test
def intersection_tiny(func, size):
    func(xrange(size / 2, size / 2 + 10))

@register_test
def intersection_small(func, size):
    func(xrange(size / 2, size / 2 + size / 10))

@register_test
def intersection_medium(func, size):
    func(xrange(size / 2, size / 2 + size * 5 / 10))

@register_test
def intersection_large(func, size):
    func(xrange(size / 2, size / 2 + size * 9 / 10))

@register_test
def intersection_update_tiny(func, size):
    func(xrange(size / 2, size / 2 + 10))

@register_test
def intersection_update_small(func, size):
    func(xrange(size / 2, size / 2 + size / 10))

@register_test
def intersection_update_medium(func, size):
    func(xrange(size / 2, size / 2 + size * 5 / 10))

@register_test
def intersection_update_large(func, size):
    func(xrange(size / 2, size / 2 + size * 9 / 10))

@register_test
def symmetric_difference_tiny(func, size):
    func(xrange(size / 2, size / 2 + 10))

@register_test
def symmetric_difference_small(func, size):
    func(xrange(size / 2, size / 2 + size / 10))

@register_test
def symmetric_difference_medium(func, size):
    func(xrange(size / 2, size / 2 + size * 5 / 10))

@register_test
def symmetric_difference_large(func, size):
    func(xrange(size / 2, size / 2 + size * 9 / 10))

@register_test
def symmetric_difference_update_tiny(func, size):
    func(xrange(size / 2, size / 2 + 10))

@register_test
def symmetric_difference_update_small(func, size):
    func(xrange(size / 2, size / 2 + size / 10))

@register_test
def symmetric_difference_update_medium(func, size):
    func(xrange(size / 2, size / 2 + size * 5 / 10))

@register_test
def symmetric_difference_update_large(func, size):
    func(xrange(size / 2, size / 2 + size * 9 / 10))

@register_test
def pop(func, size):
    for rpt in xrange(size):
        func()

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

for name, kind in kinds.items():
    impls['update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update'
    }

for name, kind in kinds.items():
    impls['update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update'
    }

for name, kind in kinds.items():
    impls['update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update'
    }

for name, kind in kinds.items():
    impls['update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update'
    }

del impls['update_tiny']['SkipListSet']
del impls['update_small']['SkipListSet']
del impls['update_medium']['SkipListSet']
del impls['update_large']['SkipListSet']

for name, kind in kinds.items():
    impls['union_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union'
    }

for name, kind in kinds.items():
    impls['union_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union'
    }

for name, kind in kinds.items():
    impls['union_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union'
    }

for name, kind in kinds.items():
    impls['union_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'union'
    }

del impls['union_tiny']['SkipListSet']
del impls['union_small']['SkipListSet']
del impls['union_medium']['SkipListSet']
del impls['union_large']['SkipListSet']

for name, kind in kinds.items():
    impls['remove'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'remove'
    }

for name, kind in kinds.items():
    impls['difference_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference'
    }

for name, kind in kinds.items():
    impls['difference_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference'
    }

for name, kind in kinds.items():
    impls['difference_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference'
    }

for name, kind in kinds.items():
    impls['difference_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference'
    }

del impls['difference_tiny']['SkipListSet']
del impls['difference_small']['SkipListSet']
del impls['difference_medium']['SkipListSet']
del impls['difference_large']['SkipListSet']

for name, kind in kinds.items():
    impls['difference_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update'
    }

for name, kind in kinds.items():
    impls['difference_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update'
    }

for name, kind in kinds.items():
    impls['difference_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update'
    }

for name, kind in kinds.items():
    impls['difference_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'difference_update'
    }

del impls['difference_update_tiny']['SkipListSet']
del impls['difference_update_small']['SkipListSet']
del impls['difference_update_medium']['SkipListSet']
del impls['difference_update_large']['SkipListSet']

for name, kind in kinds.items():
    impls['intersection_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection'
    }

for name, kind in kinds.items():
    impls['intersection_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection'
    }

for name, kind in kinds.items():
    impls['intersection_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection'
    }

for name, kind in kinds.items():
    impls['intersection_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection'
    }

del impls['intersection_tiny']['SkipListSet']
del impls['intersection_small']['SkipListSet']
del impls['intersection_medium']['SkipListSet']
del impls['intersection_large']['SkipListSet']

for name, kind in kinds.items():
    impls['intersection_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update'
    }

for name, kind in kinds.items():
    impls['intersection_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update'
    }

for name, kind in kinds.items():
    impls['intersection_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update'
    }

for name, kind in kinds.items():
    impls['intersection_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'intersection_update'
    }

del impls['intersection_update_tiny']['SkipListSet']
del impls['intersection_update_small']['SkipListSet']
del impls['intersection_update_medium']['SkipListSet']
del impls['intersection_update_large']['SkipListSet']

for name, kind in kinds.items():
    impls['symmetric_difference_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference'
    }

for name, kind in kinds.items():
    impls['symmetric_difference_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference'
    }

for name, kind in kinds.items():
    impls['symmetric_difference_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference'
    }

for name, kind in kinds.items():
    impls['symmetric_difference_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference'
    }

del impls['symmetric_difference_tiny']['SkipListSet']
del impls['symmetric_difference_small']['SkipListSet']
del impls['symmetric_difference_medium']['SkipListSet']
del impls['symmetric_difference_large']['SkipListSet']

for name, kind in kinds.items():
    impls['symmetric_difference_update_tiny'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update'
    }

for name, kind in kinds.items():
    impls['symmetric_difference_update_small'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update'
    }

for name, kind in kinds.items():
    impls['symmetric_difference_update_medium'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update'
    }

for name, kind in kinds.items():
    impls['symmetric_difference_update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'symmetric_difference_update'
    }

del impls['symmetric_difference_update_tiny']['rbset']
del impls['symmetric_difference_update_small']['rbset']
del impls['symmetric_difference_update_medium']['rbset']
del impls['symmetric_difference_update_large']['rbset']
del impls['symmetric_difference_update_tiny']['SkipListSet']
del impls['symmetric_difference_update_small']['SkipListSet']
del impls['symmetric_difference_update_medium']['SkipListSet']
del impls['symmetric_difference_update_large']['SkipListSet']

for name, kind in kinds.items():
    impls['pop'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'pop'
    }

if __name__ == '__main__':
    main()
