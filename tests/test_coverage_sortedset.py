# -*- coding: utf-8 -*-

import random
from context import sortedcontainers
from sortedcontainers import SortedSet
from nose.tools import raises

def test_init():
    temp = SortedSet(xrange(100), load=7)
    temp._check()
    assert all(val == temp[val] for val in temp)

def test_contains():
    temp = SortedSet(xrange(100), load=7)
    assert all(val in temp for val in xrange(100))
    assert all(val not in temp for val in xrange(100, 200))

def test_getitem():
    temp = SortedSet(xrange(100), load=7)
    assert all(val == temp[val] for val in temp)

def test_getitem_slice():
    vals = list(xrange(100))
    temp = SortedSet(vals, load=7)
    assert temp[20:30] == vals[20:30]

def test_delitem():
    temp = SortedSet(xrange(100), load=7)
    for val in reversed(xrange(50)):
        del temp[val]
    assert all(temp[pos] == (pos + 50) for pos in xrange(50))

def test_delitem_slice():
    vals = list(xrange(100))
    temp = SortedSet(vals, load=7)
    del vals[20:40:2]
    del temp[20:40:2]
    assert temp == vals

def test_setitem():
    temp = SortedSet(xrange(0, 1000, 10), load=7)
    temp[10] = 105

def test_setitem_slice():
    vals = list(xrange(100))
    temp = SortedSet(vals, load=7)
    temp[:25] = xrange(25)
    assert temp == vals

def test_eq():
    alpha = SortedSet(xrange(100), load=7)
    beta = SortedSet(xrange(100), load=17)
    assert alpha == beta
    beta.add(101)
    assert not (alpha == beta)

def test_ne():
    alpha = SortedSet(xrange(100), load=7)
    beta = SortedSet(xrange(99), load=17)
    assert alpha != beta
    beta[100:] = [101]
    assert alpha != beta
    beta = set(beta)
    assert alpha != beta

def test_lt_gt():
    temp = SortedSet(xrange(100), load=7)
    that = SortedSet(xrange(25, 75), load=9)
    assert that < temp
    assert temp > that

def test_le_ge():
    alpha = SortedSet(xrange(100), load=7)
    beta = SortedSet(xrange(101), load=17)
    assert alpha <= beta
    assert beta >= alpha

def test_iter():
    temp = SortedSet(xrange(100), load=7)
    assert all(val == temp[val] for val in iter(temp))

def test_len():
    temp = SortedSet(xrange(100), load=7)
    assert len(temp) == 100

def test_reversed():
    temp = SortedSet(xrange(100), load=7)
    assert all(val == temp[val] for val in temp.reversed())

def test_add():
    temp = SortedSet(xrange(100), load=7)
    temp.add(100)
    temp.add(90)
    temp._check()
    assert all(val == temp[val] for val in xrange(101))

def test_bisect():
    temp = SortedSet(xrange(100), load=7)
    assert all(temp.bisect_left(val) == val for val in xrange(100))
    assert all(temp.bisect(val) == val for val in xrange(100))
    assert all(temp.bisect_right(val) == (val + 1) for val in xrange(100))

def test_clear():
    temp = SortedSet(xrange(100), load=7)
    temp.clear()
    temp._check()
    assert len(temp) == 0

def test_copy():
    temp = SortedSet(xrange(100), load=7)
    that = temp.copy()
    that.add(1000)
    assert len(that) == 101
    assert len(temp) == 100

def test_count():
    temp = SortedSet(xrange(100), load=7)
    assert all(temp.count(val) == 1 for val in xrange(100))
    assert temp.count(100) == 0
    assert temp.count(0) == 1
    temp.add(0)
    assert temp.count(0) == 1
    temp._check()

def test_difference():
    temp = SortedSet(xrange(100), load=7)
    that = temp.difference(xrange(0, 10), xrange(10, 20))
    assert all(val == temp[val] for val in xrange(100))
    assert all((val + 20) == that[val] for val in xrange(80))

def test_difference_update():
    temp = SortedSet(xrange(100), load=7)
    temp.difference_update(xrange(0, 10), xrange(10, 20))
    assert all((val + 20) == temp[val] for val in xrange(80))

def test_discard():
    temp = SortedSet(xrange(100), load=7)
    temp.discard(0)
    temp.discard(99)
    temp.discard(50)
    temp.discard(1000)
    temp._check()
    assert len(temp) == 97

def test_index():
    temp = SortedSet(xrange(100), load=7)
    assert all(temp.index(val) == val for val in xrange(100))

def test_intersection():
    temp = SortedSet(xrange(100), load=7)
    that = temp.intersection(xrange(0, 20), xrange(10, 30))
    assert all(that[val] == (val + 10) for val in xrange(10))
    assert all(temp[val] == val for val in xrange(100))

def test_intersection_update():
    temp = SortedSet(xrange(100), load=7)
    temp.intersection_update(xrange(0, 20), xrange(10, 30))
    assert all(temp[val] == (val + 10) for val in xrange(10))

def test_isdisjoint():
    temp = SortedSet(xrange(100), load=7)
    that = SortedSet(xrange(100, 200), load=9)
    assert temp.isdisjoint(that)

def test_issubset():
    temp = SortedSet(xrange(100), load=7)
    that = SortedSet(xrange(25, 75), load=9)
    assert that.issubset(temp)

def test_issuperset():
    temp = SortedSet(xrange(100), load=7)
    that = SortedSet(xrange(25, 75), load=9)
    assert temp.issuperset(that)

def test_symmetric_difference():
    temp = SortedSet(xrange(0, 75), load=7)
    that = SortedSet(xrange(25, 100), load=9)
    result = temp.symmetric_difference(that)
    assert all(result[val] == val for val in xrange(25))
    assert all(result[val + 25] == (val + 75) for val in xrange(25))
    assert all(temp[val] == val for val in xrange(75))
    assert all(that[val] == (val + 25) for val in xrange(75))

def test_symmetric_difference_update():
    temp = SortedSet(xrange(0, 75), load=7)
    that = SortedSet(xrange(25, 100), load=9)
    temp.symmetric_difference_update(that)
    assert all(temp[val] == val for val in xrange(25))
    assert all(temp[val + 25] == (val + 75) for val in xrange(25))

def test_pop():
    temp = SortedSet(xrange(0, 100), load=7)
    temp.pop()
    temp.pop(0)
    assert all(temp[val] == (val + 1) for val in xrange(98))

def test_remove():
    temp = SortedSet(xrange(0, 100), load=7)
    temp.remove(50)

def test_union():
    temp = SortedSet(xrange(0, 50), load=7)
    that = SortedSet(xrange(50, 100), load=9)
    result = temp.union(that)
    assert all(result[val] == val for val in xrange(100))
    assert all(temp[val] == val for val in xrange(50))
    assert all(that[val] == (val + 50) for val in xrange(50))

def test_update():
    temp = SortedSet(xrange(0, 80), load=7)
    temp.update(xrange(80, 90), xrange(90, 100))
    assert all(temp[val] == val for val in xrange(100))

def test_repr():
    temp = SortedSet(xrange(0, 10), load=7)
    assert repr(temp) == 'SortedSet([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])'

if __name__ == '__main__':
    import nose
    nose.main()
