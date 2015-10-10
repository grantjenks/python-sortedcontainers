# -*- coding: utf-8 -*-

from sys import hexversion

import random
from .context import sortedcontainers
from sortedcontainers import SortedSet
from nose.tools import raises

if hexversion < 0x03000000:
    range = xrange

def negate(value):
    return -value

def modulo(value):
    return value % 10

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

def test_getitem_key():
    temp = SortedSet(range(100), load=7, key=negate)
    assert all(temp[val] == (99 - val) for val in range(100))

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
    assert temp == set(vals)

def test_delitem_key():
    temp = SortedSet(range(100), load=7, key=modulo)
    values = sorted(range(100), key=modulo)
    for val in range(10):
        del temp[val]
        del values[val]
    assert list(temp) == list(values)

def test_eq():
    alpha = SortedSet(range(100), load=7)
    beta = SortedSet(range(100), load=17)
    assert alpha == beta
    assert alpha == beta._set
    beta.add(101)
    assert not (alpha == beta)

def test_ne():
    alpha = SortedSet(range(100), load=7)
    beta = SortedSet(range(99), load=17)
    assert alpha != beta
    beta.add(100)
    assert alpha != beta
    assert alpha != beta._set
    assert alpha != list(range(101))

def test_lt_gt():
    temp = SortedSet(range(100), load=7)
    that = SortedSet(range(25, 75), load=9)
    assert that < temp
    assert not (temp < that)
    assert that < temp._set
    assert temp > that
    assert not (that > temp)
    assert temp > that._set

def test_le_ge():
    alpha = SortedSet(range(100), load=7)
    beta = SortedSet(range(101), load=17)
    assert alpha <= beta
    assert not (beta <= alpha)
    assert alpha <= beta._set
    assert beta >= alpha
    assert not (alpha >= beta)
    assert beta >= alpha._set

def test_iter():
    temp = SortedSet(range(100), load=7)
    assert all(val == temp[val] for val in iter(temp))

def test_reversed():
    temp = SortedSet(range(100), load=7)
    assert all(val == temp[val] for val in reversed(temp))

def test_islice():
    ss = SortedSet(load=7)

    assert [] == list(ss.islice())

    values = list(range(53))
    ss.update(values)

    for start in range(53):
        for stop in range(53):
            assert list(ss.islice(start, stop)) == values[start:stop]

    for start in range(53):
        for stop in range(53):
            assert list(ss.islice(start, stop, reverse=True)) == values[start:stop][::-1]

    for start in range(53):
        assert list(ss.islice(start=start)) == values[start:]
        assert list(ss.islice(start=start, reverse=True)) == values[start:][::-1]

    for stop in range(53):
        assert list(ss.islice(stop=stop)) == values[:stop]
        assert list(ss.islice(stop=stop, reverse=True)) == values[:stop][::-1]

def test_irange():
    ss = SortedSet(load=7)

    assert [] == list(ss.irange())

    values = list(range(53))
    ss.update(values)

    for start in range(53):
        for end in range(start, 53):
            assert list(ss.irange(start, end)) == values[start:(end + 1)]
            assert list(ss.irange(start, end, reverse=True)) == values[start:(end + 1)][::-1]

    for start in range(53):
        for end in range(start, 53):
            assert list(range(start, end)) == list(ss.irange(start, end, (True, False)))

    for start in range(53):
        for end in range(start, 53):
            assert list(range(start + 1, end + 1)) == list(ss.irange(start, end, (False, True)))

    for start in range(53):
        for end in range(start, 53):
            assert list(range(start + 1, end)) == list(ss.irange(start, end, (False, False)))

    for start in range(53):
        assert list(range(start, 53)) == list(ss.irange(start))

    for end in range(53):
        assert list(range(0, end)) == list(ss.irange(None, end, (True, False)))

    assert values == list(ss.irange(inclusive=(False, False)))

    assert [] == list(ss.irange(53))
    assert values == list(ss.irange(None, 53, (True, False)))

def test_irange_key():
    values = sorted(range(100), key=modulo)

    for load in range(5, 16):
        ss = SortedSet(range(100), load=load, key=modulo)

        for start in range(10):
            for end in range(start, 10):
                temp = list(ss.irange_key(start, end))
                assert temp == values[(start * 10):((end + 1) * 10)]

                temp = list(ss.irange_key(start, end, reverse=True))
                assert temp == values[(start * 10):((end + 1) * 10)][::-1]

        for start in range(10):
            for end in range(start, 10):
                temp = list(ss.irange_key(start, end, inclusive=(True, False)))
                assert temp == values[(start * 10):(end * 10)]

        for start in range(10):
            for end in range(start, 10):
                temp = list(ss.irange_key(start, end, (False, True)))
                assert temp == values[((start + 1) * 10):((end + 1) * 10)]

        for start in range(10):
            for end in range(start, 10):
                temp = list(ss.irange_key(start, end, inclusive=(False, False)))
                assert temp == values[((start + 1) * 10):(end * 10)]

        for start in range(10):
            temp = list(ss.irange_key(min_key=start))
            assert temp == values[(start * 10):]

        for end in range(10):
            temp = list(ss.irange_key(max_key=end))
            assert temp == values[:(end + 1) * 10]

def test_len():
    temp = SortedSet(range(100), load=7)
    assert len(temp) == 100

def test_add():
    temp = SortedSet(range(100), load=7)
    temp.add(100)
    temp.add(90)
    temp._check()
    assert all(val == temp[val] for val in range(101))

def test_bisect():
    temp = SortedSet(range(100), load=7)
    assert all(temp.bisect_left(val) == val for val in range(100))
    assert all(temp.bisect(val) == (val + 1) for val in range(100))
    assert all(temp.bisect_right(val) == (val + 1) for val in range(100))

def test_bisect_key():
    temp = SortedSet(range(100), key=lambda val: val, load=7)
    assert all(temp.bisect_key_left(val) == val for val in range(100))
    assert all(temp.bisect_key(val) == (val + 1) for val in range(100))
    assert all(temp.bisect_key_right(val) == (val + 1) for val in range(100))

def test_clear():
    temp = SortedSet(range(100), load=7)
    temp.clear()
    temp._check()
    assert len(temp) == 0

def test_copy():
    temp = SortedSet(range(100), load=7)
    that = temp.copy()
    that.add(1000)
    assert len(temp) == 100
    assert len(that) == 101

def test_copy_copy():
    import copy
    temp = SortedSet(range(100), load=7)
    that = copy.copy(temp)
    that.add(1000)
    assert len(temp) == 100
    assert len(that) == 101

def test_count():
    temp = SortedSet(range(100), load=7)
    assert all(temp.count(val) == 1 for val in range(100))
    assert temp.count(100) == 0
    assert temp.count(0) == 1
    temp.add(0)
    assert temp.count(0) == 1
    temp._check()

def test_sub():
    temp = SortedSet(range(100), load=7)
    that = temp - range(0, 10) - range(10, 20)
    assert all(val == temp[val] for val in range(100))
    assert all((val + 20) == that[val] for val in range(80))

def test_difference():
    temp = SortedSet(range(100), load=7)
    that = temp.difference(range(0, 10), range(10, 20))
    assert all(val == temp[val] for val in range(100))
    assert all((val + 20) == that[val] for val in range(80))

def test_difference_update():
    temp = SortedSet(range(100), load=7)
    temp.difference_update(range(0, 10), range(10, 20))
    assert all((val + 20) == temp[val] for val in range(80))

def test_isub():
    temp = SortedSet(range(100), load=7)
    temp -= range(0, 10)
    temp -= range(10, 20)
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

def test_and():
    temp = SortedSet(range(100), load=7)
    that = temp & range(20) & range(10, 30)
    assert all(that[val] == (val + 10) for val in range(10))
    assert all(temp[val] == val for val in range(100))

def test_intersection():
    temp = SortedSet(range(100), load=7)
    that = temp.intersection(range(0, 20), range(10, 30))
    assert all(that[val] == (val + 10) for val in range(10))
    assert all(temp[val] == val for val in range(100))

def test_intersection_update():
    temp = SortedSet(range(100), load=7)
    temp &= range(0, 20)
    temp &= range(10, 30)
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

def test_xor():
    temp = SortedSet(range(0, 75), load=7)
    that = SortedSet(range(25, 100), load=9)
    result = temp ^ that
    assert all(result[val] == val for val in range(25))
    assert all(result[val + 25] == (val + 75) for val in range(25))
    assert all(temp[val] == val for val in range(75))
    assert all(that[val] == (val + 25) for val in range(75))

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
    temp ^= that
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

def test_or():
    temp = SortedSet(range(0, 50), load=7)
    that = SortedSet(range(50, 100), load=9)
    result = temp | that
    assert all(result[val] == val for val in range(100))
    assert all(temp[val] == val for val in range(50))
    assert all(that[val] == (val + 50) for val in range(50))

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

def test_ior():
    temp = SortedSet(range(0, 80), load=7)
    temp |= range(80, 90)
    temp |= range(90, 100)
    assert all(temp[val] == val for val in range(100))

def test_repr():
    temp = SortedSet(range(0, 10), load=7)
    assert repr(temp) == 'SortedSet([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], key=None, load=7)'

def test_repr_recursion():
    class HashableSortedSet(SortedSet):
        def __hash__(self):
            return hash(tuple(self))

    temp = HashableSortedSet([HashableSortedSet([1]), HashableSortedSet([1, 2])])
    temp.add(temp)
    assert repr(temp) == 'HashableSortedSet([HashableSortedSet([1], key=None, load=1000), HashableSortedSet([1, 2], key=None, load=1000), ...], key=None, load=1000)'

def test_pickle():
    import pickle
    alpha = SortedSet(range(10000), key=negate, load=500)
    beta = pickle.loads(pickle.dumps(alpha))
    assert alpha == beta
    assert alpha._key == beta._key
    assert alpha._load == beta._load

if __name__ == '__main__':
    import nose
    nose.main()
