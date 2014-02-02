"""
Benchmark Sorted List Datatypes
"""

from benchmark import *

# Tests.

@register_test
def add(func, size):
    for val in lists[size]:
        func(val)

@register_test
def update(func, size):
    pos = 0
    chunk = size / 10
    while pos < size:
        func(lists[size][pos:(pos + chunk)])
        pos += chunk

@register_test
def contains(func, size):
    for val in lists[size]:
        assert func(val)

@register_test
def remove(func, size):
    for val in lists[size]:
        func(val)

@register_test
def delitem(func, size):
    while size > 0:
        pos = random.randrange(size)
        func(pos)
        size -= 1

@register_test
def getitem(func, size):
    for val in lists[size]:
        assert func(val) == val

@register_test
def pop(func, size):
    size -= 1
    while size >= 0:
        assert func() == size
        size -= 1

@register_test
def index(func, size):
    for val in lists[size]:
        assert func(val) == val

@register_test
def iter(func, size):
    count = 0
    for val in func():
        assert val == count
        count += 1

@register_test
def count(func, size):
    for val in lists[size]:
        assert func(val) == 1

# Setups.

def do_nothing(obj, size):
    pass

def fill_values(obj, size):
    obj.update(lists[size])

# Implementation imports.

from .context import sortedcontainers
from sortedcontainers import SortedList
from blist import sortedlist

kinds['SortedList'] = SortedList
kinds['blist.sortedlist'] = sortedlist

# Implementation configuration.

for name in tests:
    impls[name] = OrderedDict()

for name, kind in kinds.items():
    impls['add'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'add',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['update'][name] = {
        'setup': do_nothing,
        'ctor': kind,
        'func': 'update',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['contains'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__contains__',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['remove'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'remove',
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
    impls['getitem'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__getitem__',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['pop'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'pop',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['index'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'index',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['iter'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': '__iter__',
        'limit': 100000
    }

for name, kind in kinds.items():
    impls['count'][name] = {
        'setup': fill_values,
        'ctor': kind,
        'func': 'count',
        'limit': 100000
    }

if __name__ == '__main__':
    main('SortedList')
