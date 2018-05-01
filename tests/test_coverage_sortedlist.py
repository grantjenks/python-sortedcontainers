# -*- coding: utf-8 -*-

from sys import hexversion

import random
from .context import sortedcontainers
from sortedcontainers import SortedList
from itertools import chain
import pytest

if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

def test_init():
    slt = SortedList()
    assert slt.key is None
    slt._check()

    slt = SortedList()
    slt._reset(10000)
    assert slt._load == 10000
    slt._check()

    slt = SortedList(range(10000))
    assert all(tup[0] == tup[1] for tup in zip(slt, range(10000)))

    slt.clear()
    assert slt._len == 0
    assert slt._maxes == []
    assert slt._lists == []
    slt._check()

def test_add():
    random.seed(0)
    slt = SortedList()
    for val in range(1000):
        slt.add(val)
        slt._check()

    slt = SortedList()
    for val in range(1000, 0, -1):
        slt.add(val)
        slt._check()

    slt = SortedList()
    for val in range(1000):
        slt.add(random.random())
        slt._check()

def test_update():
    slt = SortedList()

    slt.update(range(1000))
    assert len(slt) == 1000
    slt._check()

    slt.update(range(100))
    assert len(slt) == 1100
    slt._check()

    slt.update(range(10000))
    assert len(slt) == 11100
    slt._check()

    values = sorted(chain(range(1000), range(100), range(10000)))
    assert all(tup[0] == tup[1] for tup in zip(slt, values))

def test_contains():
    slt = SortedList()
    assert 0 not in slt

    slt.update(range(10000))

    for val in range(10000):
        assert val in slt

    assert 10000 not in slt

    slt._check()

def test_discard():
    slt = SortedList()

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedList([1, 2, 2, 2, 3, 3, 5])
    slt._reset(4)

    slt.discard(6)
    slt._check()
    slt.discard(4)
    slt._check()
    slt.discard(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, [1, 2, 2, 3, 3, 5]))

def test_remove():
    slt = SortedList()

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedList([1, 2, 2, 2, 3, 3, 5])
    slt._reset(4)

    slt.remove(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, [1, 2, 2, 3, 3, 5]))

def test_remove_valueerror1():
    slt = SortedList()
    with pytest.raises(ValueError):
        slt.remove(0)

def test_remove_valueerror2():
    slt = SortedList(range(100))
    slt._reset(10)
    with pytest.raises(ValueError):
        slt.remove(100)

def test_remove_valueerror3():
    slt = SortedList([1, 2, 2, 2, 3, 3, 5])
    with pytest.raises(ValueError):
        slt.remove(4)

def test_delete():
    slt = SortedList(range(20))
    slt._reset(4)
    slt._check()
    for val in range(20):
        slt.remove(val)
        slt._check()
    assert len(slt) == 0
    assert slt._maxes == []
    assert slt._lists == []

def test_getitem():
    random.seed(0)
    slt = SortedList()
    slt._reset(17)

    lst = list()

    for rpt in range(100):
        val = random.random()
        slt.add(val)
        lst.append(val)

    lst.sort()

    assert all(slt[idx] == lst[idx] for idx in range(100))
    assert all(slt[idx - 99] == lst[idx - 99] for idx in range(100))

def test_getitem_slice():
    random.seed(0)
    slt = SortedList()
    slt._reset(17)

    lst = list()

    for rpt in range(100):
        val = random.random()
        slt.add(val)
        lst.append(val)

    lst.sort()

    assert all(slt[start:] == lst[start:]
               for start in [-75, -25, 0, 25, 75])

    assert all(slt[:stop] == lst[:stop]
               for stop in [-75, -25, 0, 25, 75])

    assert all(slt[::step] == lst[::step]
               for step in [-5, -1, 1, 5])

    assert all(slt[start:stop] == lst[start:stop]
               for start in [-75, -25, 0, 25, 75]
               for stop in [-75, -25, 0, 25, 75])

    assert all(slt[:stop:step] == lst[:stop:step]
               for stop in [-75, -25, 0, 25, 75]
               for step in [-5, -1, 1, 5])

    assert all(slt[start::step] == lst[start::step]
               for start in [-75, -25, 0, 25, 75]
               for step in [-5, -1, 1, 5])

    assert all(slt[start:stop:step] == lst[start:stop:step]
               for start in [-75, -25, 0, 25, 75]
               for stop in [-75, -25, 0, 25, 75]
               for step in [-5, -1, 1, 5])

def test_getitem_slice_big():
    slt = SortedList(range(4))
    lst = list(range(4))

    itr = ((start, stop, step)
           for start in [-6, -4, -2, 0, 2, 4, 6]
           for stop in [-6, -4, -2, 0, 2, 4, 6]
           for step in [-3, -2, -1, 1, 2, 3])

    for start, stop, step in itr:
        assert slt[start:stop:step] == lst[start:stop:step]

def test_getitem_slicezero():
    slt = SortedList(range(100))
    slt._reset(17)
    with pytest.raises(ValueError):
        slt[::0]

def test_getitem_indexerror1():
    slt = SortedList()
    with pytest.raises(IndexError):
        slt[5]

def test_getitem_indexerror2():
    slt = SortedList(range(100))
    with pytest.raises(IndexError):
        slt[200]

def test_getitem_indexerror3():
    slt = SortedList(range(100))
    with pytest.raises(IndexError):
        slt[-101]

def test_delitem():
    random.seed(0)

    slt = SortedList(range(100))
    slt._reset(17)
    while len(slt) > 0:
        pos = random.randrange(len(slt))
        del slt[pos]
        slt._check()

    slt = SortedList(range(100))
    slt._reset(17)
    del slt[:]
    assert len(slt) == 0
    slt._check()

def test_delitem_slice():
    slt = SortedList(range(100))
    slt._reset(17)
    del slt[10:40:1]
    del slt[10:40:-1]
    del slt[10:40:2]
    del slt[10:40:-2]

def test_iter():
    slt = SortedList(range(10000))
    itr = iter(slt)
    assert all(tup[0] == tup[1] for tup in zip(range(10000), itr))

def test_reversed():
    slt = SortedList(range(10000))
    rev = reversed(slt)
    assert all(tup[0] == tup[1] for tup in zip(range(9999, -1, -1), rev))

def test_reverse():
    slt = SortedList(range(10000))
    with pytest.raises(NotImplementedError):
        slt.reverse()

def test_islice():
    sl = SortedList()
    sl._reset(7)

    assert [] == list(sl.islice())

    values = list(range(53))
    sl.update(values)

    for start in range(53):
        for stop in range(53):
            assert list(sl.islice(start, stop)) == values[start:stop]

    for start in range(53):
        for stop in range(53):
            assert list(sl.islice(start, stop, reverse=True)) == values[start:stop][::-1]

    for start in range(53):
        assert list(sl.islice(start=start)) == values[start:]
        assert list(sl.islice(start=start, reverse=True)) == values[start:][::-1]

    for stop in range(53):
        assert list(sl.islice(stop=stop)) == values[:stop]
        assert list(sl.islice(stop=stop, reverse=True)) == values[:stop][::-1]

def test_irange():
    sl = SortedList()
    sl._reset(7)

    assert [] == list(sl.irange())

    values = list(range(53))
    sl.update(values)

    for start in range(53):
        for end in range(start, 53):
            assert list(sl.irange(start, end)) == values[start:(end + 1)]
            assert list(sl.irange(start, end, reverse=True)) == values[start:(end + 1)][::-1]

    for start in range(53):
        for end in range(start, 53):
            assert list(range(start, end)) == list(sl.irange(start, end, (True, False)))

    for start in range(53):
        for end in range(start, 53):
            assert list(range(start + 1, end + 1)) == list(sl.irange(start, end, (False, True)))

    for start in range(53):
        for end in range(start, 53):
            assert list(range(start + 1, end)) == list(sl.irange(start, end, (False, False)))

    for start in range(53):
        assert list(range(start, 53)) == list(sl.irange(start))

    for end in range(53):
        assert list(range(0, end)) == list(sl.irange(None, end, (True, False)))

    assert values == list(sl.irange(inclusive=(False, False)))

    assert [] == list(sl.irange(53))
    assert values == list(sl.irange(None, 53, (True, False)))

def test_len():
    slt = SortedList()

    for val in range(10000):
        slt.add(val)
        assert len(slt) == (val + 1)

def test_bisect_left():
    slt = SortedList()
    assert slt.bisect_left(0) == 0
    slt = SortedList(range(100))
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_left(50) == 100
    assert slt.bisect_left(200) == 200

def test_bisect():
    slt = SortedList()
    assert slt.bisect(10) == 0
    slt = SortedList(range(100))
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect(10) == 22
    assert slt.bisect(200) == 200

def test_bisect_right():
    slt = SortedList()
    assert slt.bisect_right(10) == 0
    slt = SortedList(range(100))
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_right(10) == 22
    assert slt.bisect_right(200) == 200

def test_copy():
    alpha = SortedList(range(100))
    alpha._reset(7)
    beta = alpha.copy()
    alpha.add(100)
    assert len(alpha) == 101
    assert len(beta) == 100

def test_copy_copy():
    import copy
    alpha = SortedList(range(100))
    alpha._reset(7)
    beta = copy.copy(alpha)
    alpha.add(100)
    assert len(alpha) == 101
    assert len(beta) == 100

def test_count():
    slt = SortedList()
    slt._reset(7)

    assert slt.count(0) == 0

    for iii in range(100):
        for jjj in range(iii):
            slt.add(iii)
        slt._check()

    for iii in range(100):
        assert slt.count(iii) == iii

    assert slt.count(100) == 0

def test_pop():
    slt = SortedList(range(10))
    slt._reset(4)
    slt._check()
    assert slt.pop() == 9
    slt._check()
    assert slt.pop(0) == 0
    slt._check()
    assert slt.pop(-2) == 7
    slt._check()
    assert slt.pop(4) == 5
    slt._check()

def test_pop_indexerror1():
    slt = SortedList(range(10))
    slt._reset(4)
    with pytest.raises(IndexError):
        slt.pop(-11)

def test_pop_indexerror2():
    slt = SortedList(range(10))
    slt._reset(4)
    with pytest.raises(IndexError):
        slt.pop(10)

def test_pop_indexerror3():
    slt = SortedList()
    with pytest.raises(IndexError):
        slt.pop()

def test_index():
    slt = SortedList(range(100))
    slt._reset(17)

    for val in range(100):
        assert val == slt.index(val)

    assert slt.index(99, 0, 1000) == 99

    slt = SortedList((0 for rpt in range(100)))
    slt._reset(17)

    for start in range(100):
        for stop in range(start, 100):
            assert slt.index(0, start, stop + 1) == start

    for start in range(100):
        assert slt.index(0, -(100 - start)) == start

    assert slt.index(0, -1000) == 0

def test_index_valueerror1():
    slt = SortedList([0] * 10)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 10)

def test_index_valueerror2():
    slt = SortedList([0] * 10)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 0, -10)

def test_index_valueerror3():
    slt = SortedList([0] * 10)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 7, 3)

def test_index_valueerror4():
    slt = SortedList([0] * 10)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(1)

def test_index_valueerror5():
    slt = SortedList()
    with pytest.raises(ValueError):
        slt.index(1)

def test_index_valueerror6():
    slt = SortedList(range(10))
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(3, 5)

def test_index_valueerror7():
    slt = SortedList([0] * 10 + [2] * 10)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(1, 0, 10)

def test_mul():
    this = SortedList(range(10))
    this._reset(4)
    that = this * 5
    this._check()
    that._check()
    assert this == list(range(10))
    assert that == sorted(list(range(10)) * 5)
    assert this != that

def test_imul():
    this = SortedList(range(10))
    this._reset(4)
    this *= 5
    this._check()
    assert this == sorted(list(range(10)) * 5)

def test_op_add():
    this = SortedList(range(10))
    this._reset(4)
    assert (this + this + this) == (this * 3)

    that = SortedList(range(10))
    that._reset(4)
    that += that
    that += that
    assert that == (this * 4)

def test_eq():
    this = SortedList(range(10))
    this._reset(4)
    assert this == list(range(10))
    assert this == tuple(range(10))
    assert not (this == list(range(9)))

def test_ne():
    this = SortedList(range(10))
    this._reset(4)
    assert this != list(range(9))
    assert this != tuple(range(11))
    assert this != [0, 1, 2, 3, 3, 5, 6, 7, 8, 9]
    assert this != (val for val in range(10))
    assert this != set()

def test_lt():
    this = SortedList(range(10, 15))
    this._reset(4)
    assert this < [10, 11, 13, 13, 14]
    assert this < [10, 11, 12, 13, 14, 15]
    assert this < [11]

def test_le():
    this = SortedList(range(10, 15))
    this._reset(4)
    assert this <= [10, 11, 12, 13, 14]
    assert this <= [10, 11, 12, 13, 14, 15]
    assert this <= [10, 11, 13, 13, 14]
    assert this <= [11]

def test_gt():
    this = SortedList(range(10, 15))
    this._reset(4)
    assert this > [10, 11, 11, 13, 14]
    assert this > [10, 11, 12, 13]
    assert this > [9]

def test_ge():
    this = SortedList(range(10, 15))
    this._reset(4)
    assert this >= [10, 11, 12, 13, 14]
    assert this >= [10, 11, 12, 13]
    assert this >= [10, 11, 11, 13, 14]
    assert this >= [9]

def test_repr():
    this = SortedList(range(10))
    this._reset(4)
    assert repr(this) == 'SortedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])'

def test_repr_recursion():
    this = SortedList([[1], [2], [3], [4]])
    this._lists[-1].append(this)
    assert repr(this) == 'SortedList([[1], [2], [3], [4], ...])'

def test_repr_subclass():
    class CustomSortedList(SortedList):
        pass
    this = CustomSortedList([1, 2, 3, 4])
    assert repr(this) == 'CustomSortedList([1, 2, 3, 4])'

def test_pickle():
    import pickle
    alpha = SortedList(range(10000))
    alpha._reset(500)
    beta = pickle.loads(pickle.dumps(alpha))
    assert alpha == beta
    assert alpha._load == beta._load

def test_build_index():
    slt = SortedList([0])
    slt._reset(4)
    slt._build_index()
    slt._check()

def test_check():
    slt = SortedList(range(10))
    slt._reset(4)
    slt._len = 5
    with pytest.raises(AssertionError):
        slt._check()
