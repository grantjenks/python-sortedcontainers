# -*- coding: utf-8 -*-

from sys import hexversion

import random
from sortedcontainers import SortedKeyList, SortedListWithKey
from itertools import chain
import pytest

if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

def negate(val):
    return -val

def test_alias():
    assert SortedKeyList is SortedListWithKey

def test_identity():
    slt = SortedKeyList(range(100))
    slt._reset(7)
    slt._check()

def test_init():
    slt = SortedKeyList(key=negate)
    slt._check()

    slt = SortedKeyList(key=negate)
    slt._reset(10000)
    assert slt._load == 10000
    slt._check()

    slt = SortedKeyList(range(10000), key=negate)
    assert all(tup[0] == tup[1] for tup in zip(slt, reversed(range(10000))))

    slt.clear()
    assert slt._len == 0
    assert slt._maxes == []
    assert slt._lists == []
    slt._check()

def test_key():
    slt = SortedKeyList(range(10000), key=lambda val: val % 10)
    slt._check()

    values = sorted(range(10000), key=lambda val: (val % 10, val))
    assert slt == values
    assert all(val in slt for val in range(10000))

def test_add():
    random.seed(0)
    slt = SortedKeyList(key=negate)
    for val in range(1000):
        slt.add(val)
        slt._check()

    slt = SortedKeyList(key=negate)
    for val in range(1000, 0, -1):
        slt.add(val)
        slt._check()

    slt = SortedKeyList(key=negate)
    for val in range(1000):
        slt.add(random.random())
        slt._check()

def test_update():
    slt = SortedKeyList(key=negate)

    slt.update(range(1000))
    assert len(slt) == 1000
    slt._check()

    slt.update(range(100))
    assert len(slt) == 1100
    slt._check()

    slt.update(range(10000))
    assert len(slt) == 11100
    slt._check()

    values = sorted((val for val in chain(range(100), range(1000), range(10000))), key=negate)
    assert all(tup[0] == tup[1] for tup in zip(slt, values))

def test_contains():
    slt = SortedKeyList(key=negate)
    assert 0 not in slt

    slt.update(range(10000))

    for val in range(10000):
        assert val in slt

    assert 10000 not in slt
    assert -1 not in slt

    slt._check()

def test_discard():
    slt = SortedKeyList(key=negate)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedKeyList([1, 2, 2, 2, 3, 3, 5], key=negate)
    slt._reset(4)

    slt.discard(6)
    slt._check()
    slt.discard(4)
    slt._check()
    slt.discard(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, reversed([1, 2, 2, 3, 3, 5])))

def test_remove():
    slt = SortedKeyList(key=negate)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedKeyList([1, 2, 2, 2, 3, 3, 5], key=negate)
    slt._reset(4)

    slt.remove(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, reversed([1, 2, 2, 3, 3, 5])))

def test_remove_valueerror1():
    slt = SortedKeyList(key=negate)
    with pytest.raises(ValueError):
        slt.remove(0)

def test_remove_valueerror2():
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(10)
    with pytest.raises(ValueError):
        slt.remove(100)

def test_remove_valueerror3():
    slt = SortedKeyList([1, 2, 2, 2, 3, 3, 5], key=negate)
    with pytest.raises(ValueError):
        slt.remove(4)

def test_delete():
    slt = SortedKeyList(range(20), key=negate)
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
    slt = SortedKeyList(key=negate)
    slt._reset(17)

    slt.add(5)
    assert slt[0] == 5
    slt.clear()

    lst = list()

    for rpt in range(100):
        val = random.random()
        slt.add(val)
        lst.append(val)

    lst.sort(reverse=True)

    assert all(slt[idx] == lst[idx] for idx in range(100))
    assert all(slt[idx - 99] == lst[idx - 99] for idx in range(100))

def test_getitem_slice():
    random.seed(0)
    slt = SortedKeyList(key=negate)
    slt._reset(17)

    lst = list()

    for rpt in range(100):
        val = random.random()
        slt.add(val)
        lst.append(val)

    lst.sort(reverse=True)

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
    slt = SortedKeyList(range(4), key=negate)
    lst = list(reversed(range(4)))

    itr = ((start, stop, step)
           for start in [-6, -4, -2, 0, 2, 4, 6]
           for stop in [-6, -4, -2, 0, 2, 4, 6]
           for step in [-3, -2, -1, 1, 2, 3])

    for start, stop, step in itr:
        assert slt[start:stop:step] == lst[start:stop:step]

def test_getitem_slicezero():
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(17)
    with pytest.raises(ValueError):
        slt[::0]

def test_getitem_indexerror1():
    slt = SortedKeyList(key=negate)
    with pytest.raises(IndexError):
        slt[5]

def test_getitem_indexerror2():
    slt = SortedKeyList(range(100), key=negate)
    with pytest.raises(IndexError):
        slt[200]

def test_getitem_indexerror3():
    slt = SortedKeyList(range(100), key=negate)
    with pytest.raises(IndexError):
        slt[-101]

def test_delitem():
    random.seed(0)
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(17)
    while len(slt) > 0:
        del slt[random.randrange(len(slt))]
        slt._check()

def test_delitem_slice():
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(17)
    del slt[10:40:1]
    del slt[10:40:-1]
    del slt[10:40:2]
    del slt[10:40:-2]

def test_iter():
    slt = SortedKeyList(range(10000), key=negate)
    itr = iter(slt)
    assert all(tup[0] == tup[1] for tup in zip(range(9999, -1, -1), itr))

def test_reversed():
    slt = SortedKeyList(range(10000), key=negate)
    rev = reversed(slt)
    assert all(tup[0] == tup[1] for tup in zip(range(10000), rev))

def test_reverse():
    slt = SortedKeyList(range(10000), key=negate)
    with pytest.raises(NotImplementedError):
        slt.reverse()

def test_islice():
    return
    slt = SortedKeyList(key=negate)
    slt._reset(7)

    assert [] == list(slt.islice())

    values = sorted(range(53), key=negate)
    slt.update(values)

    for start in range(53):
        for stop in range(53):
            assert list(slt.islice(start, stop)) == values[start:stop]

    for start in range(53):
        for stop in range(53):
            assert list(slt.islice(start, stop, reverse=True)) == values[start:stop][::-1]

    for start in range(53):
        assert list(slt.islice(start=start)) == values[start:]
        assert list(slt.islice(start=start, reverse=True)) == values[start:][::-1]

    for stop in range(53):
        assert list(slt.islice(stop=stop)) == values[:stop]
        assert list(slt.islice(stop=stop, reverse=True)) == values[:stop][::-1]

def test_irange():
    slt = SortedKeyList(key=negate)
    slt._reset(7)

    assert [] == list(slt.irange())

    values = list(range(53))
    slt.update(values)

    for start in range(53):
        for end in range(start, 53):
            assert list(slt.irange(end, start)) == values[start:(end + 1)][::-1]
            assert list(slt.irange(end, start, reverse=True)) == values[start:(end + 1)]

    for start in range(53):
        for end in range(start, 53):
            assert list(slt.irange(end, start, (True, False))) == values[(start + 1):(end + 1)][::-1]

    for start in range(53):
        for end in range(start, 53):
            assert list(slt.irange(end, start, (False, True))) == values[start:end][::-1]

    for start in range(53):
        for end in range(start, 53):
            assert list(slt.irange(end, start, (False, False))) == values[(start + 1):end][::-1]

    for start in range(53):
        assert list(slt.irange(start)) == values[:(start + 1)][::-1]

    for end in range(53):
        assert list(slt.irange(None, end, (True, False))) == values[(end + 1):][::-1]

    assert list(slt.irange(inclusive=(False, False))) == values[::-1]

    assert list(slt.irange(-1)) == []
    assert list(slt.irange(None, -1, (True, False))) == values[::-1]

def test_len():
    slt = SortedKeyList(key=negate)

    for val in range(10000):
        slt.add(val)
        assert len(slt) == (val + 1)

def test_bisect_left():
    slt = SortedKeyList(key=negate)
    assert slt.bisect_left(0) == 0
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_left(50) == 98
    assert slt.bisect_left(0) == 198
    assert slt.bisect_left(-1) == 200

def test_bisect():
    slt = SortedKeyList(key=negate)
    assert slt.bisect(10) == 0
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect(10) == 180
    assert slt.bisect(0) == 200

def test_bisect_right():
    slt = SortedKeyList(key=negate)
    assert slt.bisect_right(10) == 0
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(17)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_right(10) == 180
    assert slt.bisect_right(0) == 200

def test_copy():
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(7)
    two = slt.copy()
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_copy_copy():
    import copy
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(7)
    two = copy.copy(slt)
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_count():
    slt = SortedKeyList(key=negate)
    slt._reset(7)

    assert slt.count(0) == 0

    for iii in range(100):
        for jjj in range(iii):
            slt.add(iii)
        slt._check()

    for iii in range(100):
        assert slt.count(iii) == iii

def test_pop():
    slt = SortedKeyList(range(10), key=negate)
    slt._reset(4)
    slt._check()
    assert slt.pop() == 0
    slt._check()
    assert slt.pop(0) == 9
    slt._check()
    assert slt.pop(-2) == 2
    slt._check()
    assert slt.pop(4) == 4
    slt._check()

def test_pop_indexerror1():
    slt = SortedKeyList(range(10), key=negate)
    slt._reset(4)
    with pytest.raises(IndexError):
        slt.pop(-11)

def test_pop_indexerror2():
    slt = SortedKeyList(range(10), key=negate)
    slt._reset(4)
    with pytest.raises(IndexError):
        slt.pop(10)

def test_index():
    slt = SortedKeyList(range(100), key=negate)
    slt._reset(17)

    for pos, val in enumerate(range(99, -1, -1)):
        assert val == slt.index(pos)

    assert slt.index(99, 0, 1000) == 0

    slt = SortedKeyList((0 for rpt in range(100)), key=negate)
    slt._reset(17)

    for start in range(100):
        for stop in range(start, 100):
            assert slt.index(0, start, stop + 1) == start

    for start in range(100):
        assert slt.index(0, -(100 - start)) == start

    assert slt.index(0, -1000) == 0

def test_index_valueerror1():
    slt = SortedKeyList([0] * 10, key=negate)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 10)

def test_index_valueerror2():
    slt = SortedKeyList([0] * 10, key=negate)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 0, -10)

def test_index_valueerror3():
    slt = SortedKeyList([0] * 10, key=negate)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(0, 7, 3)

def test_index_valueerror4():
    slt = SortedKeyList([0] * 10, key=negate)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(1)

def test_index_valueerror5():
    slt = SortedKeyList(key=negate)
    with pytest.raises(ValueError):
        slt.index(1)

def test_index_valueerror6():
    slt = SortedKeyList(range(10), key=negate)
    slt._reset(4)
    with pytest.raises(ValueError):
        slt.index(6, 5)

def test_mul():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    that = this * 5
    this._check()
    that._check()
    assert this == list(reversed((range(10))))
    assert that == list(sorted(list(range(10)) * 5, reverse=True))
    assert this != that

def test_imul():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    this *= 5
    this._check()
    assert this == sorted(list(range(10)) * 5, reverse=True)

def test_op_add():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    assert (this + this + this) == (this * 3)

    that = SortedKeyList(range(10), key=negate)
    that._reset(4)
    that += that
    that += that
    assert that == (this * 4)

def test_eq():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    that = SortedKeyList(range(20), key=negate)
    that._reset(4)
    assert not (this == that)
    that.clear()
    that.update(range(10))
    assert this == that

def test_lt():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    that = SortedKeyList(range(10, 20), key=negate)
    that._reset(5)
    assert this < that
    assert not (that < this)
    that = SortedKeyList(range(1, 20), key=negate)
    that._reset(6)
    assert this < that
    that = SortedKeyList(range(1, 10), key=negate)
    that._reset(4)
    assert not (this < that)

def test_lte():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    that = SortedKeyList(range(10), key=negate)
    that._reset(5)
    assert this <= that
    assert that <= this
    del this[-1]
    assert this <= that
    assert not (that <= this)

def test_gt():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    that = SortedKeyList(range(10, 20), key=negate)
    that._reset(5)
    assert that > this
    assert not (this > that)
    that = SortedKeyList(range(1, 20), key=negate)
    that._reset(6)
    assert that > this
    that = SortedKeyList(range(1, 10), key=negate)
    that._reset(4)
    assert not (that > this)

def test_gte():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    that = SortedKeyList(range(10), key=negate)
    that._reset(5)
    assert this >= that
    assert that >= this
    del this[-1]
    assert that >= this
    assert not (this >= that)

def test_repr():
    this = SortedKeyList(range(10), key=negate)
    this._reset(4)
    assert repr(this).startswith('SortedKeyList([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], key=<function negate at ')

def test_pickle():
    import pickle
    alpha = SortedKeyList(range(10000), key=negate)
    alpha._reset(500)
    beta = pickle.loads(pickle.dumps(alpha))
    assert alpha == beta
    assert alpha._key == beta._key
    assert alpha._load == 500
    assert beta._load == 1000

def test_check():
    slt = SortedKeyList(range(10), key=negate)
    slt._reset(4)
    slt._len = 5
    with pytest.raises(AssertionError):
        slt._check()
