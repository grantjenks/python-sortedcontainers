# -*- coding: utf-8 -*-

from sys import hexversion

import random
from .context import sortedcontainers
from sortedcontainers import SortedList, SortedListWithKey
from nose.tools import raises

if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

def modulo(val):
    return val % 10

def test_init():
    slt = SortedListWithKey(key=modulo)
    slt._check()

    slt = SortedListWithKey(load=10000, key=modulo)
    assert slt._load == 10000
    assert slt._twice == 20000
    assert slt._half == 5000
    slt._check()

    slt = SortedListWithKey(range(10000), key=modulo)
    assert all(tup[0] == tup[1] for tup in zip(slt, sorted(range(10000), key=modulo)))

    slt.clear()
    assert slt._len == 0
    assert slt._maxes == []
    assert slt._lists == []

    assert isinstance(slt, SortedList)
    assert isinstance(slt, SortedListWithKey)

    slt._check()

def test_new():
    slt = SortedList(key=modulo)
    slt._check()

    assert isinstance(slt, SortedList)
    assert isinstance(slt, SortedListWithKey)
    assert type(slt) == SortedListWithKey

    slt = SortedListWithKey(key=modulo)
    slt._check()

    assert isinstance(slt, SortedList)
    assert isinstance(slt, SortedListWithKey)
    assert type(slt) == SortedListWithKey

@raises(TypeError)
def test_new_error():
    class SortedListPlus(SortedList):
        pass
    SortedListPlus(key=modulo)

def test_key():
    slt = SortedListWithKey(range(10000), key=lambda val: val % 10)
    slt._check()

    values = sorted(range(10000), key=lambda val: (val % 10, val))
    assert slt == values
    assert all(val in slt for val in range(10000))

def test_key2():
    class Incomparable:
        pass
    a = Incomparable()
    b = Incomparable()
    slt = SortedListWithKey(key=lambda val: 1)
    slt.add(a)
    slt.add(b)
    assert slt == [a, b]

def test_add():
    random.seed(0)
    slt = SortedListWithKey(key=modulo)
    for val in range(1000):
        slt.add(val)
    slt._check()

    slt = SortedListWithKey(key=modulo)
    for val in range(1000, 0, -1):
        slt.add(val)
    slt._check()

    slt = SortedListWithKey(key=modulo)
    for val in range(1000):
        slt.add(random.random())
    slt._check()

def test_update():
    slt = SortedListWithKey(key=modulo)

    slt.update(range(1000))
    assert all(tup[0] == tup[1] for tup in zip(slt, sorted(range(1000), key=modulo)))
    assert len(slt) == 1000
    slt._check()

    slt.update(range(10000))
    assert len(slt) == 11000
    slt._check()

def test_contains():
    slt = SortedListWithKey(key=modulo, load=7)

    assert 0 not in slt

    slt.update(range(100))

    for val in range(100):
        assert val in slt

    assert 100 not in slt

    slt._check()

    slt = SortedListWithKey(range(100), key=modulo, load=4)
    assert all(val not in slt for val in range(100, 200))

def test_discard():
    slt = SortedListWithKey(key=modulo)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedListWithKey([1, 2, 2, 2, 3, 3, 5], load=4, key=modulo)

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
    slt = SortedListWithKey(key=modulo)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedListWithKey([1, 2, 2, 2, 3, 3, 5], load=4, key=modulo)

    slt.remove(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, [1, 2, 2, 3, 3, 5]))

@raises(ValueError)
def test_remove_valueerror1():
    slt = SortedListWithKey(key=modulo)
    slt.remove(0)

@raises(ValueError)
def test_remove_valueerror2():
    slt = SortedListWithKey(range(100), load=10, key=modulo)
    slt.remove(100)

@raises(ValueError)
def test_remove_valueerror3():
    slt = SortedListWithKey([1, 2, 2, 2, 3, 3, 5], key=modulo)
    slt.remove(4)

@raises(ValueError)
def test_remove_valueerror4():
    slt = SortedListWithKey([1, 1, 1, 2, 2, 2], key=modulo)
    slt.remove(13)

@raises(ValueError)
def test_remove_valueerror5():
    slt = SortedListWithKey([1, 1, 1, 2, 2, 2], key=modulo)
    slt.remove(12)

def test_delete():
    slt = SortedListWithKey(range(20), load=4, key=modulo)
    slt._check()
    for val in range(20):
        slt.remove(val)
        slt._check()
    assert len(slt) == 0
    assert slt._maxes == []
    assert slt._lists == []

def test_getitem():
    random.seed(0)
    slt = SortedListWithKey(load=17, key=modulo)

    slt.append(5)
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
    slt = SortedListWithKey(load=17, key=modulo)

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
    slt = SortedListWithKey(range(4), key=modulo)
    lst = sorted(range(4), key=modulo)

    itr = ((start, stop, step)
           for start in [-6, -4, -2, 0, 2, 4, 6]
           for stop in [-6, -4, -2, 0, 2, 4, 6]
           for step in [-3, -2, -1, 1, 2, 3])

    for start, stop, step in itr:
        assert slt[start:stop:step] == lst[start:stop:step]

@raises(ValueError)
def test_getitem_slicezero():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt[::0]

@raises(IndexError)
def test_getitem_indexerror1():
    slt = SortedListWithKey(key=modulo)
    slt[5]

@raises(IndexError)
def test_getitem_indexerror2():
    slt = SortedListWithKey(range(100), key=modulo)
    slt[200]

@raises(IndexError)
def test_getitem_indexerror3():
    slt = SortedListWithKey(range(100), key=modulo)
    slt[-101]

def test_delitem():
    random.seed(0)

    slt = SortedListWithKey(range(100), load=17, key=modulo)
    while len(slt) > 0:
        del slt[random.randrange(len(slt))]
        slt._check()

    slt = SortedListWithKey(range(100), load=17, key=modulo)
    del slt[:]
    assert len(slt) == 0
    slt._check()

def test_delitem_slice():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    del slt[10:40:1]
    del slt[10:40:-1]
    del slt[10:40:2]
    del slt[10:40:-2]

def test_setitem():
    random.seed(0)
    slt = SortedListWithKey(range(0, 100), load=17, key=modulo)
    slt[0] = 100
    slt[99] = 99
    slt[55] = 45

def test_setitem_slice():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt[:10] = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    slt[:10:2] = [0, 10, 20, 30, 40]
    slt[:] = sorted(range(100), key=modulo)
    slt[90:] = []
    slt[:10] = []
    assert len(slt) == 80

@raises(ValueError)
def test_setitem_slice_bad():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt[:10] = list(reversed(range(10)))

@raises(ValueError)
def test_setitem_slice_bad1():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt[10:20] = range(20, 30)

@raises(ValueError)
def test_setitem_slice_bad2():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt[20:30] = range(10, 20)

@raises(ValueError)
def test_setitem_extended_slice_bad1():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt[20:80:3] = list(range(10))

@raises(ValueError)
def test_setitem_extended_slice_bad2():
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt[40:90:5] = list(range(10))

@raises(ValueError)
def test_setitem_valueerror1():
    slt = SortedListWithKey(range(10), key=modulo)
    slt[9] = 10

@raises(ValueError)
def test_setitem_valueerror2():
    slt = SortedListWithKey(range(10), key=modulo)
    slt[0] = 9

def test_iter():
    slt = SortedListWithKey(range(10000), key=modulo)
    itr = iter(slt)
    assert all(tup[0] == tup[1] for tup in zip(sorted(range(10000), key=modulo), itr))

def test_reversed():
    slt = SortedListWithKey(range(10000), key=modulo)
    rev = reversed(slt)
    assert all(tup[0] == tup[1] for tup in zip(reversed(sorted(range(10000), key=modulo)), rev))

def test_islice():
    sl = SortedListWithKey(load=7, key=modulo)

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
        slt = SortedListWithKey(range(100), load=load, key=modulo)

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
        slt = SortedListWithKey(range(100), load=load, key=modulo)

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
    slt = SortedListWithKey(key=modulo)

    for val in range(10000):
        slt.add(val)
        assert len(slt) == (val + 1)

def test_bisect_left():
    slt = SortedListWithKey(key=modulo)
    assert slt.bisect_left(0) == 0
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_left(50) == 0
    assert slt.bisect_left(0) == 0

def test_bisect():
    slt = SortedListWithKey(key=modulo)
    assert slt.bisect(10) == 0
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt.update(range(100))
    slt._check()
    assert slt.bisect(10) == 20
    assert slt.bisect(0) == 20

def test_bisect_right():
    slt = SortedListWithKey(key=modulo)
    assert slt.bisect_right(10) == 0
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_right(10) == 20
    assert slt.bisect_right(0) == 20

def test_bisect_key_left():
    slt = SortedListWithKey(key=modulo)
    assert slt.bisect_key_left(10) == 0
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_key_left(0) == 0
    assert slt.bisect_key_left(5) == 100
    assert slt.bisect_key_left(10) == 200

def test_bisect_key_right():
    slt = SortedListWithKey(key=modulo)
    assert slt.bisect_key_right(0) == 0
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_key_right(0) == 20
    assert slt.bisect_key_right(5) == 120
    assert slt.bisect_key_right(10) == 200

def test_bisect_key():
    slt = SortedListWithKey(key=modulo)
    assert slt.bisect_key(0) == 0
    slt = SortedListWithKey(range(100), load=17, key=modulo)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_key(0) == 20
    assert slt.bisect_key(5) == 120
    assert slt.bisect_key(10) == 200

def test_copy():
    slt = SortedListWithKey(range(100), load=7, key=modulo)
    two = slt.copy()
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_copy_copy():
    import copy
    slt = SortedListWithKey(range(100), load=7, key=modulo)
    two = copy.copy(slt)
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_count():
    slt = SortedListWithKey(load=7, key=modulo)

    assert slt.count(0) == 0

    for iii in range(100):
        for jjj in range(iii):
            slt.add(iii)
    slt._check()

    for iii in range(100):
        assert slt.count(iii) == iii

    slt = SortedListWithKey(range(8), key=modulo)
    assert slt.count(9) == 0

def test_append():
    slt = SortedListWithKey(load=4, key=modulo)

    slt.append(0)

    for val in range(1, 10):
        slt.append(val)
        slt._check()

@raises(ValueError)
def test_append_valueerror():
    slt = SortedListWithKey(range(100), key=modulo)
    slt.append(5)

def test_extend():
    slt = SortedListWithKey(load=4, key=modulo)

    slt.extend(range(5))
    slt._check()

    slt.extend(range(6, 10))
    slt._check()

@raises(ValueError)
def test_extend_valueerror1():
    slt = SortedListWithKey(key=modulo)
    slt.extend([1, 2, 3, 5, 4, 6])

@raises(ValueError)
def test_extend_valueerror2():
    slt = SortedListWithKey(range(20), load=4, key=modulo)
    slt.extend([17, 18, 19, 20, 21, 22, 23])

def test_insert():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.insert(-100, 0)
    slt._check()
    slt.insert(-1, 9)
    slt._check()
    slt.insert(0, 10)
    slt._check()

    slt = SortedListWithKey(load=4, key=modulo)
    slt.insert(0, 5)
    slt._check()

    slt = SortedListWithKey(range(5, 15), load=4, key=modulo)
    for rpt in range(8):
        slt.insert(0, 10)
        slt._check()

    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.insert(8, 8)
    slt._check()

@raises(ValueError)
def test_insert_valueerror1():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.insert(10, 5)

@raises(ValueError)
def test_insert_valueerror2():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.insert(0, 9)

@raises(ValueError)
def test_insert_valueerror3():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.insert(5, 3)

@raises(ValueError)
def test_insert_valueerror4():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.insert(5, 7)

def test_pop():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt._check()
    assert slt.pop() == 9
    slt._check()
    assert slt.pop(0) == 0
    slt._check()
    assert slt.pop(-2) == 7
    slt._check()
    assert slt.pop(4) == 5
    slt._check()

@raises(IndexError)
def test_pop_indexerror1():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.pop(-11)

@raises(IndexError)
def test_pop_indexerror2():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.pop(10)

def test_index():
    slt = SortedListWithKey(range(100), load=7, key=modulo)

    for pos, val in enumerate(sorted(range(100), key=modulo)):
        assert val == slt.index(pos)

    assert slt.index(9, 0, 1000) == 90

    slt = SortedListWithKey((0 for rpt in range(100)), load=7, key=modulo)

    for start in range(100):
        for stop in range(start, 100):
            assert slt.index(0, start, stop + 1) == start

    for start in range(100):
        assert slt.index(0, -(100 - start)) == start

    assert slt.index(0, -1000) == 0

@raises(ValueError)
def test_index_valueerror1():
    slt = SortedListWithKey([0] * 10, load=4, key=modulo)
    slt.index(0, 10)

@raises(ValueError)
def test_index_valueerror2():
    slt = SortedListWithKey([0] * 10, load=4, key=modulo)
    slt.index(0, 0, -10)

@raises(ValueError)
def test_index_valueerror3():
    slt = SortedListWithKey([0] * 10, load=4, key=modulo)
    slt.index(0, 7, 3)

@raises(ValueError)
def test_index_valueerror4():
    slt = SortedListWithKey([0] * 10, load=4, key=modulo)
    slt.index(1)

@raises(ValueError)
def test_index_valueerror5():
    slt = SortedListWithKey(key=modulo)
    slt.index(1)

@raises(ValueError)
def test_index_valueerror6():
    slt = SortedListWithKey(range(100), load=4, key=modulo)
    slt.index(91, 0, 15)

@raises(ValueError)
def test_index_valueerror7():
    slt = SortedListWithKey([0] * 10 + [1] * 10 + [2] * 10, load=4, key=modulo)
    slt.index(1, 0, 10)

@raises(ValueError)
def test_index_valueerror8():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.index(4, 5)

@raises(ValueError)
def test_index_valueerror9():
    slt = SortedListWithKey(load=4, key=modulo)
    slt.index(5)

@raises(ValueError)
def test_index_valueerror10():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt.index(19)

def test_mul():
    this = SortedListWithKey(range(10), load=4, key=modulo)
    that = this * 5
    this._check()
    that._check()
    assert this == sorted(range(10), key=modulo)
    assert that == sorted(list(range(10)) * 5, key=modulo)
    assert this != that

def test_imul():
    this = SortedListWithKey(range(10), load=4, key=modulo)
    this *= 5
    this._check()
    assert this == sorted(list(range(10)) * 5, key=modulo)

def test_op_add():
    this = SortedListWithKey(range(10), load=4, key=modulo)
    assert (this + this + this) == (this * 3)

    that = SortedListWithKey(range(10), load=4, key=modulo)
    that += that
    that += that
    assert that == (this * 4)

def test_eq():
    this = SortedListWithKey(range(10), load=4, key=modulo)
    assert this == list(range(10))
    assert this == tuple(range(10))
    assert not (this == list(range(9)))

def test_ne():
    this = SortedListWithKey(range(10, 20), load=4, key=modulo)
    assert this != list(range(11, 21))
    assert this != tuple(range(10, 21))
    assert this != [0, 1, 2, 3, 3, 5, 6, 7, 8, 9]
    assert this != (val for val in range(10))
    assert this != set()

def test_lt():
    this = SortedListWithKey(range(10, 15), load=4, key=modulo)
    assert this < [10, 11, 13, 13, 14]
    assert this < [10, 11, 12, 13, 14, 15]
    assert this < [11]

def test_le():
    this = SortedListWithKey(range(10, 15), load=4, key=modulo)
    assert this <= [10, 11, 12, 13, 14]
    assert this <= [10, 11, 12, 13, 14, 15]
    assert this <= [10, 11, 13, 13, 14]
    assert this <= [11]

def test_gt():
    this = SortedListWithKey(range(10, 15), load=4, key=modulo)
    assert this > [10, 11, 11, 13, 14]
    assert this > [10, 11, 12, 13]
    assert this > [9]

def test_ge():
    this = SortedListWithKey(range(10, 15), load=4, key=modulo)
    assert this >= [10, 11, 12, 13, 14]
    assert this >= [10, 11, 12, 13]
    assert this >= [10, 11, 11, 13, 14]
    assert this >= [9]

def test_repr():
    this = SortedListWithKey(range(10), load=4, key=modulo)
    assert repr(this).startswith('SortedListWithKey([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], key=<function modulo at ')

def test_repr_recursion():
    this = SortedListWithKey([[1], [2], [3], [4]], key=lambda val: val)
    this._lists[-1].append(this)
    assert repr(this).startswith('SortedListWithKey([[1], [2], [3], [4], ...], key=<function ')

def test_repr_subclass():
    class CustomSortedListWithKey(SortedListWithKey):
        pass
    this = CustomSortedListWithKey(range(10), load=4, key=modulo)
    assert repr(this).startswith('CustomSortedListWithKey([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], key=<function modulo at ')

@raises(AssertionError)
def test_check():
    slt = SortedListWithKey(range(10), load=4, key=modulo)
    slt._len = 5
    slt._check()

if __name__ == '__main__':
    import nose
    nose.main()
