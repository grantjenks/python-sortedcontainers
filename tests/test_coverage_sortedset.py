# -*- coding: utf-8 -*-

from sys import version_info

import random
from .context import sortedcontainers
from sortedcontainers import SortedSet
from nose.tools import raises

if version_info[0] == 2:
    range = xrange

def test_init():
    temp = SortedSet(range(100), load=7)
    temp._check()
    assert all(val == temp[val] for val in temp)

def test_contains():
    temp = SortedSet(range(100), load=7)
    assert all(val in temp for val in range(100))
    assert all(val not in temp for val in range(100, 200))

def test_getitem():
    temp = SortedSet(range(100), load=7)
    assert all(val == temp[val] for val in temp)

def test_getitem_slice():
    vals = list(range(100))
    temp = SortedSet(vals, load=7)
    assert temp[20:30] == vals[20:30]

def test_delitem():
    temp = SortedSet(range(100), load=7)
    for val in reversed(range(50)):
        del temp[val]
    assert all(temp[pos] == (pos + 50) for pos in range(50))

def test_delitem_slice():
    vals = list(range(100))
    temp = SortedSet(vals, load=7)
    del vals[20:40:2]
    del temp[20:40:2]
    assert temp == vals

def test_setitem():
    temp = SortedSet(range(0, 1000, 10), load=7)
    temp[10] = 105

def test_setitem_slice():
    vals = list(range(100))
    temp = SortedSet(vals, load=7)
    temp[:25] = range(25)
    assert temp == vals

def test_eq():
    alpha = SortedSet(range(100), load=7)
    beta = SortedSet(range(100), load=17)
    assert alpha == beta
    assert alpha == beta._set
    assert alpha == list(beta)
    beta.add(101)
    assert not (alpha == beta)

def test_ne():
    alpha = SortedSet(range(100), load=7)
    beta = SortedSet(range(99), load=17)
    assert alpha != beta
    assert alpha != beta._set
    assert alpha != list(beta)
    beta[100:] = [101]
    assert alpha != beta
    beta = set(beta)
    assert alpha != beta

def test_lt_gt():
    temp = SortedSet(range(100), load=7)
    that = SortedSet(range(25, 75), load=9)
    assert that < temp
    assert temp > that

def test_le_ge():
    alpha = SortedSet(range(100), load=7)
    beta = SortedSet(range(101), load=17)
    assert alpha <= beta
    assert beta >= alpha

def test_iter():
    temp = SortedSet(range(100), load=7)
    assert all(val == temp[val] for val in iter(temp))

def test_len():
    temp = SortedSet(range(100), load=7)
    assert len(temp) == 100

def test_reversed():
    temp = SortedSet(range(100), load=7)
    assert all(val == temp[val] for val in reversed(temp))

def test_add():
    temp = SortedSet(range(100), load=7)
    temp.add(100)
    temp.add(90)
    temp._check()
    assert all(val == temp[val] for val in range(101))

def test_bisect():
    temp = SortedSet(range(100), load=7)
    assert all(temp.bisect_left(val) == val for val in range(100))
    assert all(temp.bisect(val) == val for val in range(100))
    assert all(temp.bisect_right(val) == (val + 1) for val in range(100))

def test_clear():
    temp = SortedSet(range(100), load=7)
    temp.clear()
    temp._check()
    assert len(temp) == 0

def test_copy():
    temp = SortedSet(range(100), load=7)
    that = temp.copy()
    that.add(1000)
    assert len(that) == 101
    assert len(temp) == 101

def test_count():
    temp = SortedSet(range(100), load=7)
    assert all(temp.count(val) == 1 for val in range(100))
    assert temp.count(100) == 0
    assert temp.count(0) == 1
    temp.add(0)
    assert temp.count(0) == 1
    temp._check()

def test_difference():
    temp = SortedSet(range(100), load=7)
    that = temp.difference(range(0, 10), range(10, 20))
    assert all(val == temp[val] for val in range(100))
    assert all((val + 20) == that[val] for val in range(80))

def test_difference_update():
    temp = SortedSet(range(100), load=7)
    temp.difference_update(range(0, 10), range(10, 20))
    assert all((val + 20) == temp[val] for val in range(80))

def test_discard():
    temp = SortedSet(range(100), load=7)
    temp.discard(0)
    temp.discard(99)
    temp.discard(50)
    temp.discard(1000)
    temp._check()
    assert len(temp) == 97

def test_index():
    temp = SortedSet(range(100), load=7)
    assert all(temp.index(val) == val for val in range(100))

def test_intersection():
    temp = SortedSet(range(100), load=7)
    that = temp.intersection(range(0, 20), range(10, 30))
    assert all(that[val] == (val + 10) for val in range(10))
    assert all(temp[val] == val for val in range(100))

def test_intersection_update():
    temp = SortedSet(range(100), load=7)
    temp.intersection_update(range(0, 20), range(10, 30))
    assert all(temp[val] == (val + 10) for val in range(10))

def test_isdisjoint():
    temp = SortedSet(range(100), load=7)
    that = SortedSet(range(100, 200), load=9)
    assert temp.isdisjoint(that)

def test_issubset():
    temp = SortedSet(range(100), load=7)
    that = SortedSet(range(25, 75), load=9)
    assert that.issubset(temp)

def test_issuperset():
    temp = SortedSet(range(100), load=7)
    that = SortedSet(range(25, 75), load=9)
    assert temp.issuperset(that)

def test_symmetric_difference():
    temp = SortedSet(range(0, 75), load=7)
    that = SortedSet(range(25, 100), load=9)
    result = temp.symmetric_difference(that)
    assert all(result[val] == val for val in range(25))
    assert all(result[val + 25] == (val + 75) for val in range(25))
    assert all(temp[val] == val for val in range(75))
    assert all(that[val] == (val + 25) for val in range(75))

def test_symmetric_difference_update():
    temp = SortedSet(range(0, 75), load=7)
    that = SortedSet(range(25, 100), load=9)
    temp.symmetric_difference_update(that)
    assert all(temp[val] == val for val in range(25))
    assert all(temp[val + 25] == (val + 75) for val in range(25))

def test_pop():
    temp = SortedSet(range(0, 100), load=7)
    temp.pop()
    temp.pop(0)
    assert all(temp[val] == (val + 1) for val in range(98))

def test_remove():
    temp = SortedSet(range(0, 100), load=7)
    temp.remove(50)

def test_union():
    temp = SortedSet(range(0, 50), load=7)
    that = SortedSet(range(50, 100), load=9)
    result = temp.union(that)
    assert all(result[val] == val for val in range(100))
    assert all(temp[val] == val for val in range(50))
    assert all(that[val] == (val + 50) for val in range(50))

def test_update():
    temp = SortedSet(range(0, 80), load=7)
    temp.update(range(80, 90), range(90, 100))
    assert all(temp[val] == val for val in range(100))

def test_repr():
    temp = SortedSet(range(0, 10), load=7)
    assert repr(temp) == 'SortedSet([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])'

def test_repr_recursion():
    class HashableSortedSet(SortedSet):
        def __hash__(self):
            return hash(tuple(self))

    temp = HashableSortedSet([HashableSortedSet([1]), HashableSortedSet([1, 2])])
    temp.add(temp)
    assert repr(temp) == 'HashableSortedSet([HashableSortedSet([1]), HashableSortedSet([1, 2]), ...])'

if __name__ == '__main__':
    import nose
    nose.main()
