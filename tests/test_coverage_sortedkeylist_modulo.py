# -*- coding: utf-8 -*-

from sys import hexversion

import random
from sortedcontainers import SortedList, SortedKeyList
import pytest

if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

def modulo(val):
    return val % 10

def test_init():
    slt = SortedKeyList(key=modulo)
    assert slt.key == modulo
    slt._check()

    slt = SortedKeyList(key=modulo)
    slt._reset(10000)
    assert slt._load == 10000
    slt._check()

    slt = SortedKeyList(range(10000), key=modulo)
    assert all(tup[0] == tup[1] for tup in zip(slt, sorted(range(10000), key=modulo)))

    slt.clear()
    assert slt._len == 0
    assert slt._maxes == []
    assert slt._lists == []

    assert isinstance(slt, SortedList)
    assert isinstance(slt, SortedKeyList)

    slt._check()

def test_new():
    slt = SortedList(iter(range(1000)), key=modulo)
    assert slt == sorted(range(1000), key=modulo)
    slt._check()

    assert isinstance(slt, SortedList)
    assert isinstance(slt, SortedKeyList)
    assert type(slt) == SortedKeyList

    slt = SortedKeyList(iter(range(1000)), key=modulo)
    assert slt == sorted(range(1000), key=modulo)
    slt._check()

    assert isinstance(slt, SortedList)
    assert isinstance(slt, SortedKeyList)
    assert type(slt) == SortedKeyList

def test_new_error():
    class SortedListPlus(SortedList):
        pass
    with pytest.raises(TypeError):
        SortedListPlus(key=modulo)

def test_key():
    slt = SortedKeyList(range(10000), key=lambda val: val % 10)
    slt._check()

    values = sorted(range(10000), key=lambda val: (val % 10, val))
    assert slt == values
    assert all(val in slt for val in range(10000))

def test_key2():
    class Incomparable:
        pass
    a = Incomparable()
    b = Incomparable()
    slt = SortedKeyList(key=lambda val: 1)
    slt.add(a)
    slt.add(b)
    assert slt == [a, b]

def test_add():
    random.seed(0)
    slt = SortedKeyList(key=modulo)
    for val in range(1000):
        slt.add(val)
    slt._check()

    slt = SortedKeyList(key=modulo)
    for val in range(1000, 0, -1):
        slt.add(val)
    slt._check()

    slt = SortedKeyList(key=modulo)
    for val in range(1000):
        slt.add(random.random())
    slt._check()

def test_update():
    slt = SortedKeyList(key=modulo)

    slt.update(range(1000))
    assert all(tup[0] == tup[1] for tup in zip(slt, sorted(range(1000), key=modulo)))
    assert len(slt) == 1000
    slt._check()

    slt.update(range(10000))
    assert len(slt) == 11000
    slt._check()

def test_contains():
    slt = SortedKeyList(key=modulo)
    slt._reset(7)

    assert 0 not in slt

    slt.update(range(100))

    for val in range(100):
        assert val in slt

    assert 100 not in slt

    slt._check()

    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(4)
    assert all(val not in slt for val in range(100, 200))

def test_discard():
    slt = SortedKeyList(key=modulo)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedKeyList([1, 2, 2, 2, 3, 3, 5], key=modulo)
    slt._reset(4)

    slt.discard(6)
    slt._check()
    slt.discard(4)
    slt._check()
    slt.discard(2)
    slt._check()
    slt.discard(11)
    slt.discard(12)
    slt.discard(13)
    slt.discard(15)

    assert all(tup[0] == tup[1] for tup in zip(slt, [1, 2, 2, 3, 3, 5]))

def test_remove():
    slt = SortedKeyList(key=modulo)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedKeyList([1, 2, 2, 2, 3, 3, 5], key=modulo)
    slt._reset(4)

    slt.remove(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, [1, 2, 2, 3, 3, 5]))

def test_remove_valueerror1():
    slt = SortedKeyList(key=modulo)
    with pytest.raises(ValueError):
        slt.remove(0)

def test_remove_valueerror2():
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(10)
    with pytest.raises(ValueError):
        slt.remove(100)

def test_remove_valueerror3():
    slt = SortedKeyList([1, 2, 2, 2, 3, 3, 5], key=modulo)
    with pytest.raises(ValueError):
        slt.remove(4)

def test_remove_valueerror4():
    slt = SortedKeyList([1, 1, 1, 2, 2, 2], key=modulo)
    with pytest.raises(ValueError):
        slt.remove(13)

def test_remove_valueerror5():
    slt = SortedKeyList([1, 1, 1, 2, 2, 2], key=modulo)
    with pytest.raises(ValueError):
        slt.remove(12)

def test_delete():
    slt = SortedKeyList(range(20), key=modulo)
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
    slt = SortedKeyList(key=modulo)
    slt._reset(17)

    slt.add(5)
    slt._build_index()
    slt._check()
    slt.clear()

    lst = list(random.random() for rpt in range(100))
    slt.update(lst)
    lst.sort(key=modulo)

    assert all(slt[idx] == lst[idx] for idx in range(100))
    assert all(slt[idx - 99] == lst[idx - 99] for idx in range(100))

def test_getitem_slice():
    random.seed(0)
    slt = SortedKeyList(key=modulo)
    slt._reset(17)

    lst = list()

    for rpt in range(100):
        val = random.random()
        slt.add(val)
        lst.append(val)

    lst.sort(key=modulo)

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
    slt = SortedKeyList(range(4), key=modulo)
    lst = sorted(range(4), key=modulo)

    itr = ((start, stop, step)
           for start in [-6, -4, -2, 0, 2, 4, 6]
           for stop in [-6, -4, -2, 0, 2, 4, 6]
           for step in [-3, -2, -1, 1, 2, 3])

    for start, stop, step in itr:
        assert slt[start:stop:step] == lst[start:stop:step]

def test_getitem_slicezero():
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    with pytest.raises(ValueError):
        slt[::0]

def test_getitem_indexerror1():
    slt = SortedKeyList(key=modulo)
    with pytest.raises(IndexError):
        slt[5]

def test_getitem_indexerror2():
    slt = SortedKeyList(range(100), key=modulo)
    with pytest.raises(IndexError):
        slt[200]

def test_getitem_indexerror3():
    slt = SortedKeyList(range(100), key=modulo)
    with pytest.raises(IndexError):
        slt[-101]

def test_delitem():
    random.seed(0)

    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    while len(slt) > 0:
        del slt[random.randrange(len(slt))]
        slt._check()

    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    del slt[:]
    assert len(slt) == 0
    slt._check()

def test_delitem_slice():
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    del slt[10:40:1]
    del slt[10:40:-1]
    del slt[10:40:2]
    del slt[10:40:-2]

def test_iter():
    slt = SortedKeyList(range(10000), key=modulo)
    itr = iter(slt)
    assert all(tup[0] == tup[1] for tup in zip(sorted(range(10000), key=modulo), itr))

def test_reversed():
    slt = SortedKeyList(range(10000), key=modulo)
    rev = reversed(slt)
    assert all(tup[0] == tup[1] for tup in zip(reversed(sorted(range(10000), key=modulo)), rev))

def test_reverse():
    slt = SortedKeyList(range(10000), key=modulo)
    with pytest.raises(NotImplementedError):
        slt.reverse()

def test_islice():
    sl = SortedKeyList(key=modulo)
    sl._reset(7)

    assert [] == list(sl.islice())

    values = sorted(range(100), key=modulo)
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
    values = sorted(range(100), key=modulo)

    for load in range(5, 16):
        slt = SortedKeyList(range(100), key=modulo)
        slt._reset(load)

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange(start, end))
                assert temp == values[(start * 10):((end + 1) * 10)]

                temp = list(slt.irange(start, end, reverse=True))
                assert temp == values[(start * 10):((end + 1) * 10)][::-1]

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange(start, end, inclusive=(True, False)))
                assert temp == values[(start * 10):(end * 10)]

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange(start, end, (False, True)))
                assert temp == values[((start + 1) * 10):((end + 1) * 10)]

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange(start, end, inclusive=(False, False)))
                assert temp == values[((start + 1) * 10):(end * 10)]

        for start in range(10):
            temp = list(slt.irange(minimum=start))
            assert temp == values[(start * 10):]

        for end in range(10):
            temp = list(slt.irange(maximum=end))
            assert temp == values[:(end + 1) * 10]

def test_irange_key():
    values = sorted(range(100), key=modulo)

    for load in range(5, 16):
        slt = SortedKeyList(range(100), key=modulo)
        slt._reset(load)

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange_key(start, end))
                assert temp == values[(start * 10):((end + 1) * 10)]

                temp = list(slt.irange_key(start, end, reverse=True))
                assert temp == values[(start * 10):((end + 1) * 10)][::-1]

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange_key(start, end, inclusive=(True, False)))
                assert temp == values[(start * 10):(end * 10)]

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange_key(start, end, (False, True)))
                assert temp == values[((start + 1) * 10):((end + 1) * 10)]

        for start in range(10):
            for end in range(start, 10):
                temp = list(slt.irange_key(start, end, inclusive=(False, False)))
                assert temp == values[((start + 1) * 10):(end * 10)]

        for start in range(10):
            temp = list(slt.irange_key(min_key=start))
            assert temp == values[(start * 10):]

        for end in range(10):
            temp = list(slt.irange_key(max_key=end))
            assert temp == values[:(end + 1) * 10]

def test_len():
    slt = SortedKeyList(key=modulo)

    for val in range(10000):
        slt.add(val)
        assert len(slt) == (val + 1)

def test_bisect_left():
    slt = SortedKeyList(key=modulo)
    assert slt.bisect_left(0) == 0
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_left(50) == 0
    assert slt.bisect_left(0) == 0

def test_bisect():
    slt = SortedKeyList(key=modulo)
    assert slt.bisect(10) == 0
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect(10) == 20
    assert slt.bisect(0) == 20

def test_bisect_right():
    slt = SortedKeyList(key=modulo)
    assert slt.bisect_right(10) == 0
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_right(10) == 20
    assert slt.bisect_right(0) == 20

def test_bisect_key_left():
    slt = SortedKeyList(key=modulo)
    assert slt.bisect_key_left(10) == 0
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_key_left(0) == 0
    assert slt.bisect_key_left(5) == 100
    assert slt.bisect_key_left(10) == 200

def test_bisect_key_right():
    slt = SortedKeyList(key=modulo)
    assert slt.bisect_key_right(0) == 0
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_key_right(0) == 20
    assert slt.bisect_key_right(5) == 120
    assert slt.bisect_key_right(10) == 200

def test_bisect_key():
    slt = SortedKeyList(key=modulo)
    assert slt.bisect_key(0) == 0
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_key(0) == 20
    assert slt.bisect_key(5) == 120
    assert slt.bisect_key(10) == 200

def test_copy():
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(7)
    two = slt.copy()
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_copy_copy():
    import copy
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(7)
    two = copy.copy(slt)
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_count():
    slt = SortedKeyList(key=modulo)
    slt._reset(7)

    assert slt.count(0) == 0

    for iii in range(100):
        for jjj in range(iii):
            slt.add(iii)
    slt._check()

    for iii in range(100):
        assert slt.count(iii) == iii

    slt = SortedKeyList(range(8), key=modulo)
    assert slt.count(9) == 0

def test_pop():
    slt = SortedKeyList(range(10), key=modulo)
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
    slt = SortedKeyList(range(10), key=modulo)
    slt._reset(4)
    with pytest.raises(IndexError):
        slt.pop(-11)

def test_pop_indexerror2():
    slt = SortedKeyList(range(10), key=modulo)
    slt._reset(4)
    with pytest.raises(IndexError):
        slt.pop(10)

def test_index():
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(7)

    for pos, val in enumerate(sorted(range(100), key=modulo)):
        assert val == slt.index(pos)

    assert slt.index(9, 0, 1000) == 90

    slt = SortedKeyList((0 for rpt in range(100)), key=modulo)
    slt._reset(7)

    for start in range(100):
        for stop in range(start, 100):
            assert slt.index(0, start, stop + 1) == start

    for start in range(100):
        assert slt.index(0, -(100 - start)) == start

    assert slt.index(0, -1000) == 0

def test_index_valueerror1():
    slt = SortedKeyList([0] * 10, key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 10)

def test_index_valueerror2():
    slt = SortedKeyList([0] * 10, key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 0, -10)

def test_index_valueerror3():
    slt = SortedKeyList([0] * 10, key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 7, 3)

def test_index_valueerror4():
    slt = SortedKeyList([0] * 10, key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(1)

def test_index_valueerror5():
    slt = SortedKeyList(key=modulo)
    with pytest.raises(ValueError):
        slt.index(1)

def test_index_valueerror6():
    slt = SortedKeyList(range(100), key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(91, 0, 15)

def test_index_valueerror7():
    slt = SortedKeyList([0] * 10 + [1] * 10 + [2] * 10, key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(1, 0, 10)

def test_index_valueerror8():
    slt = SortedKeyList(range(10), key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(4, 5)

def test_index_valueerror9():
    slt = SortedKeyList(key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(5)

def test_index_valueerror10():
    slt = SortedKeyList(range(10), key=modulo)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(19)

def test_mul():
    this = SortedKeyList(range(10), key=modulo)
    this._reset(4)
    that = this * 5
    this._check()
    that._check()
    assert this == sorted(range(10), key=modulo)
    assert that == sorted(list(range(10)) * 5, key=modulo)
    assert this != that

def test_imul():
    this = SortedKeyList(range(10), key=modulo)
    this._reset(4)
    this *= 5
    this._check()
    assert this == sorted(list(range(10)) * 5, key=modulo)

def test_op_add():
    this = SortedKeyList(range(10), key=modulo)
    this._reset(4)
    assert (this + this + this) == (this * 3)

    that = SortedKeyList(range(10), key=modulo)
    that._reset(4)
    that += that
    that += that
    assert that == (this * 4)

def test_eq():
    this = SortedKeyList(range(10), key=modulo)
    this._reset(4)
    assert this == list(range(10))
    assert this == tuple(range(10))
    assert not (this == list(range(9)))

def test_ne():
    this = SortedKeyList(range(10, 20), key=modulo)
    this._reset(4)
    assert this != list(range(11, 21))
    assert this != tuple(range(10, 21))
    assert this != [0, 1, 2, 3, 3, 5, 6, 7, 8, 9]
    assert this != (val for val in range(10))
    assert this != set()

def test_lt():
    this = SortedKeyList(range(10, 15), key=modulo)
    this._reset(4)
    assert this < [10, 11, 13, 13, 14]
    assert this < [10, 11, 12, 13, 14, 15]
    assert this < [11]

def test_le():
    this = SortedKeyList(range(10, 15), key=modulo)
    this._reset(4)
    assert this <= [10, 11, 12, 13, 14]
    assert this <= [10, 11, 12, 13, 14, 15]
    assert this <= [10, 11, 13, 13, 14]
    assert this <= [11]

def test_gt():
    this = SortedKeyList(range(10, 15), key=modulo)
    this._reset(4)
    assert this > [10, 11, 11, 13, 14]
    assert this > [10, 11, 12, 13]
    assert this > [9]

def test_ge():
    this = SortedKeyList(range(10, 15), key=modulo)
    this._reset(4)
    assert this >= [10, 11, 12, 13, 14]
    assert this >= [10, 11, 12, 13]
    assert this >= [10, 11, 11, 13, 14]
    assert this >= [9]

def test_repr():
    this = SortedKeyList(range(10), key=modulo)
    this._reset(4)
    assert repr(this).startswith('SortedKeyList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], key=<function modulo at ')

def test_repr_recursion():
    this = SortedKeyList([[1], [2], [3], [4]], key=lambda val: val)
    this._lists[-1].append(this)
    assert repr(this).startswith('SortedKeyList([[1], [2], [3], [4], ...], key=<function ')

def test_repr_subclass():
    class CustomSortedKeyList(SortedKeyList):
        pass
    this = CustomSortedKeyList(range(10), key=modulo)
    this._reset(4)
    assert repr(this).startswith('CustomSortedKeyList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], key=<function modulo at ')

def test_check():
    slt = SortedKeyList(range(10), key=modulo)
    slt._reset(4)
    slt._len = 5
    with pytest.raises(AssertionError):
        slt._check()
