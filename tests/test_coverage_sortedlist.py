# -*- coding: utf-8 -*-

import random
from context import sortedcontainers
from sortedcontainers import SortedList
from nose.tools import raises
from itertools import izip

def test_init():
    slt = SortedList()
    slt._check()

    slt = SortedList(load=10000)
    assert slt._load == 10000
    assert slt._twice == 20000
    assert slt._half == 5000
    slt._check()

    slt = SortedList(xrange(10000))
    assert all(tup[0] == tup[1] for tup in izip(slt, xrange(10000)))

    slt.clear()
    assert slt._len == 0
    assert slt._maxes == None
    assert slt._lists == []
    slt._check()

def test_add():
    random.seed(0)
    slt = SortedList()
    for val in xrange(1000):
        slt.add(val)
        slt._check()

    slt = SortedList()
    for val in xrange(1000, 0, -1):
        slt.add(val)
        slt._check()

    slt = SortedList()
    for val in xrange(1000):
        slt.add(random.random())
        slt._check()

def test_update():
    slt = SortedList()

    slt.update(xrange(1000))
    assert all(tup[0] == tup[1] for tup in izip(slt, list(xrange(1000))))
    assert len(slt) == 1000
    slt._check()

    slt.update(xrange(10000))
    assert len(slt) == 11000
    slt._check()

def test_contains():
    slt = SortedList()
    assert 0 not in slt

    slt.update(xrange(10000))

    for val in xrange(10000):
        assert val in slt

    assert 10000 not in slt

    slt._check()

def test_discard():
    slt = SortedList()

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedList([1, 2, 2, 2, 3, 3, 5], load=4)

    slt.discard(6)
    slt._check()
    slt.discard(4)
    slt._check()
    slt.discard(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in izip(slt, [1, 2, 2, 3, 3, 5]))

def test_remove():
    slt = SortedList()

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedList([1, 2, 2, 2, 3, 3, 5], load=4)

    slt.discard(6)
    slt._check()
    slt.discard(4)
    slt._check()
    slt.discard(2)

    assert all(tup[0] == tup[1] for tup in izip(slt, [1, 2, 2, 3, 3, 5]))

@raises(ValueError)
def test_remove_valueerror1():
    slt = SortedList()
    slt.remove(0)

@raises(ValueError)
def test_remove_valueerror2():
    slt = SortedList(xrange(100), load=10)
    slt.remove(100)

@raises(ValueError)
def test_remove_valueerror3():
    slt = SortedList([1, 2, 2, 2, 3, 3, 5])
    slt.remove(4)

def test_delete():
    slt = SortedList(xrange(20), load=4)
    slt._check()
    for val in xrange(20):
        slt.remove(val)
        slt._check()
    assert len(slt) == 0
    assert slt._maxes == None
    assert slt._lists == []

def test_getitem():
    random.seed(0)
    slt = SortedList(load=17)

    lst = list()

    for rpt in xrange(100):
        val = random.random()
        slt.add(val)
        lst.append(val)

    lst.sort()

    assert all(slt[idx] == lst[idx] for idx in xrange(100))
    assert all(slt[idx - 99] == lst[idx - 99] for idx in xrange(100))

def test_getitem_slice():
    random.seed(0)
    slt = SortedList(load=17)

    lst = list()

    for rpt in xrange(100):
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
    slt = SortedList(xrange(4))
    lst = list(xrange(4))

    itr = ((start, stop, step)
           for start in [-6, -4, -2, 0, 2, 4, 6]
           for stop in [-6, -4, -2, 0, 2, 4, 6]
           for step in [-3, -2, -1, 1, 2, 3])

    for start, stop, step in itr:
        print start, stop, step
        assert slt[start:stop:step] == lst[start:stop:step]

@raises(ValueError)
def test_getitem_slicezero():
    slt = SortedList(xrange(100), load=17)
    slt[::0]

@raises(IndexError)
def test_getitem_indexerror1():
    slt = SortedList()
    slt[5]

@raises(IndexError)
def test_getitem_indexerror2():
    slt = SortedList(xrange(100))
    slt[200]

@raises(IndexError)
def test_getitem_indexerror3():
    slt = SortedList(xrange(100))
    slt[-101]

def test_delitem():
    random.seed(0)
    slt = SortedList(xrange(100), load=17)
    while len(slt) > 0:
        del slt[random.randrange(len(slt))]
        slt._check()

def test_delitem_slice():
    slt = SortedList(xrange(100), load=17)
    del slt[10:40:1]
    del slt[10:40:-1]
    del slt[10:40:2]
    del slt[10:40:-2]

def test_setitem():
    random.seed(0)
    slt = SortedList(xrange(0, 100, 10), load=4)

    values = list(enumerate(xrange(5, 105, 10)))
    random.shuffle(values)
    for pos, val in values:
        slt[pos] = val

def test_setitem_slice():
    slt = SortedList(xrange(100), load=17)
    slt[:10] = iter(xrange(10))
    assert slt == list(xrange(100))
    slt[:10:2] = iter(val * 2 for val in xrange(5))
    assert slt == list(xrange(100))
    slt[:50] = xrange(-50, 50)
    assert slt == list(xrange(-50, 100))
    slt[:100] = xrange(50)
    assert slt == list(xrange(100))
    slt[:] = xrange(100)
    assert slt == list(xrange(100))

@raises(ValueError)
def test_setitem_slice_bad():
    slt = SortedList(xrange(100), load=17)
    slt[:10] = list(reversed(xrange(10)))

@raises(ValueError)
def test_setitem_slice_bad1():
    slt = SortedList(xrange(100), load=17)
    slt[10:20] = xrange(20, 30)

@raises(ValueError)
def test_setitem_slice_bad2():
    slt = SortedList(xrange(100), load=17)
    slt[20:30] = xrange(10, 20)

def test_setitem_extended_slice():
    slt = SortedList(xrange(0, 1000, 10), load=17)
    lst = list(xrange(0, 1000, 10))
    lst[10:90:10] = xrange(105, 905, 100)
    slt[10:90:10] = xrange(105, 905, 100)
    assert slt == lst

@raises(ValueError)
def test_setitem_extended_slice_bad1():
    slt = SortedList(xrange(100), load=17)
    slt[20:80:3] = list(xrange(10))

@raises(ValueError)
def test_setitem_extended_slice_bad2():
    slt = SortedList(xrange(100), load=17)
    slt[40:90:5] = list(xrange(10))

@raises(ValueError)
def test_setitem_valueerror1():
    slt = SortedList(xrange(10))
    slt[9] = 0

@raises(ValueError)
def test_setitem_valueerror2():
    slt = SortedList(xrange(10))
    slt[0] = 10

def test_iter():
    slt = SortedList(xrange(10000))
    itr = iter(slt)
    assert all(tup[0] == tup[1] for tup in izip(xrange(10000), itr))

def test_reversed():
    slt = SortedList(xrange(10000))
    rev = slt.reversed()
    assert all(tup[0] == tup[1] for tup in izip(xrange(9999, -1, -1), rev))

def test_len():
    slt = SortedList()

    for val in xrange(10000):
        slt.add(val)
        assert len(slt) == (val + 1)

def test_bisect_left():
    slt = SortedList()
    assert slt.bisect_left(0) == 0
    slt = SortedList(xrange(100), load=17)
    slt.update(xrange(100))
    slt._check()
    assert slt.bisect_left(50) == 100
    assert slt.bisect_left(200) == 200

def test_bisect():
    slt = SortedList()
    assert slt.bisect(0) == 0
    slt = SortedList(xrange(100), load=17)
    slt.update(xrange(100))
    slt._check()
    assert slt.bisect(50) == 100
    assert slt.bisect(200) == 200

def test_bisect_right():
    slt = SortedList()
    assert slt.bisect_right(10) == 0
    slt = SortedList(xrange(100), load=17)
    slt.update(xrange(100))
    slt._check()
    assert slt.bisect_right(10) == 22
    assert slt.bisect_right(200) == 200

def test_count():
    slt = SortedList(load=7)

    assert slt.count(0) == 0

    for iii in xrange(100):
        for jjj in xrange(iii):
            slt.add(iii)
        slt._check()

    for iii in xrange(100):
        assert slt.count(iii) == iii

def test_append():
    slt = SortedList(load=17)

    slt.append(0)

    for val in xrange(1, 1000):
        slt.append(val)
        slt._check()

@raises(ValueError)
def test_append_valueerror():
    slt = SortedList(xrange(100))
    slt.append(5)

def test_extend():
    slt = SortedList(load=17)

    slt.extend(xrange(100))
    slt._check()

    slt.extend(list(xrange(100, 200)))
    slt._check()

    for val in xrange(200, 300):
        slt.extend([val] * (val - 199))
        slt._check()

@raises(ValueError)
def test_extend_valueerror1():
    slt = SortedList()
    slt.extend([1, 2, 3, 5, 4, 6])

@raises(ValueError)
def test_extend_valueerror2():
    slt = SortedList(xrange(20), load=4)
    slt.extend([17, 18, 19, 20, 21, 22, 23])

def test_insert():
    slt = SortedList(xrange(10), load=4)
    slt.insert(-1, 9)
    slt._check()
    slt.insert(-100, 0)
    slt._check()
    slt.insert(100, 10)
    slt._check()

    slt = SortedList(load=4)
    slt.insert(0, 5)
    slt._check()

    slt = SortedList(xrange(5, 15), load=4)
    for rpt in xrange(8):
        slt.insert(0, 4)
        slt._check()

    slt = SortedList(xrange(10), load=4)
    slt.insert(8, 8)
    slt._check()

@raises(ValueError)
def test_insert_valueerror1():
    slt = SortedList(xrange(10), load=4)
    slt.insert(10, 5)

@raises(ValueError)
def test_insert_valueerror2():
    slt = SortedList(xrange(10), load=4)
    slt.insert(0, 10)

@raises(ValueError)
def test_insert_valueerror3():
    slt = SortedList(xrange(10), load=4)
    slt.insert(5, 3)

@raises(ValueError)
def test_insert_valueerror4():
    slt = SortedList(xrange(10), load=4)
    slt.insert(5, 7)

def test_pop():
    slt = SortedList(xrange(10), load=4)
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
    slt = SortedList(xrange(10), load=4)
    slt.pop(-11)

@raises(IndexError)
def test_pop_indexerror2():
    slt = SortedList(xrange(10), load=4)
    slt.pop(10)

def test_index():
    slt = SortedList(xrange(100), load=17)

    for val in xrange(100):
        assert val == slt.index(val)

    assert slt.index(99, 0, 1000) == 99

    slt = SortedList((0 for rpt in xrange(100)), load=17)

    for start in xrange(100):
        for stop in xrange(start, 100):
            assert slt.index(0, start, stop + 1) == start

    for start in xrange(100):
        assert slt.index(0, -(100 - start)) == start

    assert slt.index(0, -1000) == 0

@raises(ValueError)
def test_index_valueerror1():
    slt = SortedList([0] * 10, load=4)
    slt.index(0, 10)

@raises(ValueError)
def test_index_valueerror2():
    slt = SortedList([0] * 10, load=4)
    slt.index(0, 0, -10)

@raises(ValueError)
def test_index_valueerror3():
    slt = SortedList([0] * 10, load=4)
    slt.index(0, 7, 3)

@raises(ValueError)
def test_index_valueerror4():
    slt = SortedList([0] * 10, load=4)
    slt.index(1)

@raises(ValueError)
def test_index_valueerror5():
    slt = SortedList()
    slt.index(1)

@raises(ValueError)
def test_index_valueerror6():
    slt = SortedList(xrange(10), load=4)
    slt.index(3, 5)

def test_mul():
    this = SortedList(xrange(10), load=4)
    that = this * 5
    this._check()
    that._check()
    assert this == list(xrange(10))
    assert that == sorted(list(xrange(10)) * 5)
    assert this != that

def test_imul():
    this = SortedList(xrange(10), load=4)
    this *= 5
    this._check()
    assert this == sorted(list(xrange(10)) * 5)

def test_op_add():
    this = SortedList(xrange(10), load=4)
    assert (this + this + this) == (this * 3)

    that = SortedList(xrange(10), load=4)
    that += that
    that += that
    assert that == (this * 4)

def test_eq():
    this = SortedList(xrange(10), load=4)
    that = SortedList(xrange(20), load=4)
    assert not (this == that)
    that.clear()
    that.update(xrange(10))
    assert this == that

def test_lt():
    this = SortedList(xrange(10), load=4)
    that = SortedList(xrange(10, 20), load=5)
    assert this < that
    assert not (that < this)
    that = SortedList(xrange(1, 20), load=6)
    assert this < that
    that = SortedList(xrange(1, 10), load=4)
    assert not (this < that)

def test_lte():
    this = SortedList(xrange(10), load=4)
    that = SortedList(xrange(10), load=5)
    assert this <= that
    assert that <= this
    del this[-1]
    assert this <= that
    assert not (that <= this)

def test_gt():
    this = SortedList(xrange(10), load=4)
    that = SortedList(xrange(10, 20), load=5)
    assert that > this
    assert not (this > that)
    that = SortedList(xrange(1, 20), load=6)
    assert that > this
    that = SortedList(xrange(1, 10), load=4)
    assert not (that > this)

def test_gte():
    this = SortedList(xrange(10), load=4)
    that = SortedList(xrange(10), load=5)
    assert this >= that
    assert that >= this
    del this[-1]
    assert that >= this
    assert not (this >= that)

def test_repr():
    this = SortedList(xrange(10), load=4)
    assert repr(this) == 'SortedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])'

@raises(AssertionError)
def test_check():
    slt = SortedList(xrange(10), load=4)
    slt._len = 5
    slt._check()

if __name__ == '__main__':
    import nose
    nose.main()
