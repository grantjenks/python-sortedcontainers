"""
Benchmark Sorted List Datatypes
"""

import warnings
from .benchmark import *

# Tests.

@register_test
def add(func, size):
    for val in lists[size][::100]:
        func(val)

@register_test
def update_small(func, size):
    func(lists[size][::10])

@register_test
def update_large(func, size):
    func(lists[size])

@register_test
def contains(func, size):
    for val in lists[size][::100]:
        assert func(val)

@register_test
def remove(func, size):
    for val in lists[size][::100]:
        func(val)

@register_test
def delitem(func, size):
    for val in range(int(size / 100)):
        pos = random.randrange(size - val)
        func(pos)

@register_test
def bisect(func, size):
    for val in lists[size][::100]:
        func(val)

@register_test
def getitem(func, size):
    for val in lists[size][::100]:
        assert func(val) == val

@register_test
def pop(func, size):
    for val in range(int(size / 100)):
        assert func() == (size - val - 1)

@register_test
def index(func, size):
    for val in lists[size][::100]:
        assert func(val) == val

@register_test
def iter(func, size):
    assert all(idx == val for idx, val in enumerate(func()))

@register_test
def count(func, size):
    for val in lists[size][::100]:
        assert func(val) == 1

# Setups.

def do_nothing(obj, size):
    pass

def fill_values(obj, size):
    obj.update(sorted(lists[size]))

# Implementation imports.

from .context import sortedcontainers
from sortedcontainers import SortedList
kinds['SortedList'] = SortedList

try:
    from blist import sortedlist
    kinds['blist.sortedlist'] = sortedlist
except ImportError:
    warnings.warn('No module named blist', ImportWarning)

# Implementation configuration.

for name in tests:
    impls[name] = OrderedDict()

for name, kind in kinds.items():
    impls['add'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'add',
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
    impls['update_large'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'update',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['contains'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__contains__',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['remove'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'remove',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['delitem'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__delitem__',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['bisect'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'bisect',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['getitem'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__getitem__',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['pop'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'pop',
        'limit': 1000000
    }

for name, kind in kinds.items():
    impls['index'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'index',
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
    impls['count'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'count',
        'limit': 1000000
    }

if __name__ == '__main__':
    main('SortedList')
