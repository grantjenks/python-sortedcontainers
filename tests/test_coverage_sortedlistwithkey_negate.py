# -*- coding: utf-8 -*-

from sys import hexversion

import random
from .context import sortedcontainers
from sortedcontainers import SortedListWithKey
from itertools import chain
from nose.tools import raises

if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

def negate(val):
    return -val

def test_identity():
    slt = SortedListWithKey(range(100), load=7)
    slt._check()

def test_init():
    slt = SortedListWithKey(key=negate)
    slt._check()

    slt = SortedListWithKey(load=10000, key=negate)
    assert slt._load == 10000
    assert slt._twice == 20000
    assert slt._half == 5000
    slt._check()

    slt = SortedListWithKey(range(10000), key=negate)
    assert all(tup[0] == tup[1] for tup in zip(slt, reversed(range(10000))))

    slt.clear()
    assert slt._len == 0
    assert slt._maxes == []
    assert slt._lists == []
    slt._check()

def test_key():
    slt = SortedListWithKey(range(10000), key=lambda val: val % 10)
    slt._check()

    values = sorted(range(10000), key=lambda val: (val % 10, val))
    assert slt == values
    assert all(val in slt for val in range(10000))

def test_add():
    random.seed(0)
    slt = SortedListWithKey(key=negate)
    for val in range(1000):
        slt.add(val)
        slt._check()

    slt = SortedListWithKey(key=negate)
    for val in range(1000, 0, -1):
        slt.add(val)
        slt._check()

    slt = SortedListWithKey(key=negate)
    for val in range(1000):
        slt.add(random.random())
        slt._check()

def test_update():
    slt = SortedListWithKey(key=negate)

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
    slt = SortedListWithKey(key=negate)
    assert 0 not in slt

    slt.update(range(10000))

    for val in range(10000):
        assert val in slt

    assert 10000 not in slt
    assert -1 not in slt

    slt._check()

def test_discard():
    slt = SortedListWithKey(key=negate)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedListWithKey([1, 2, 2, 2, 3, 3, 5], load=4, key=negate)

    slt.discard(6)
    slt._check()
    slt.discard(4)
    slt._check()
    slt.discard(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, reversed([1, 2, 2, 3, 3, 5])))

def test_remove():
    slt = SortedListWithKey(key=negate)

    assert slt.discard(0) == None
    assert len(slt) == 0
    slt._check()

    slt = SortedListWithKey([1, 2, 2, 2, 3, 3, 5], load=4, key=negate)

    slt.remove(2)
    slt._check()

    assert all(tup[0] == tup[1] for tup in zip(slt, reversed([1, 2, 2, 3, 3, 5])))

@raises(ValueError)
def test_remove_valueerror1():
    slt = SortedListWithKey(key=negate)
    slt.remove(0)

@raises(ValueError)
def test_remove_valueerror2():
    slt = SortedListWithKey(range(100), load=10, key=negate)
    slt.remove(100)

@raises(ValueError)
def test_remove_valueerror3():
    slt = SortedListWithKey([1, 2, 2, 2, 3, 3, 5], key=negate)
    slt.remove(4)

def test_delete():
    slt = SortedListWithKey(range(20), load=4, key=negate)
    slt._check()
    for val in range(20):
        slt.remove(val)
        slt._check()
    assert len(slt) == 0
    assert slt._maxes == []
    assert slt._lists == []

def test_getitem():
    random.seed(0)
    slt = SortedListWithKey(load=17, key=negate)

    slt.append(5)
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
    slt = SortedListWithKey(load=17, key=negate)

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
    slt = SortedListWithKey(range(4), key=negate)
    lst = list(reversed(range(4)))

    itr = ((start, stop, step)
           for start in [-6, -4, -2, 0, 2, 4, 6]
           for stop in [-6, -4, -2, 0, 2, 4, 6]
           for step in [-3, -2, -1, 1, 2, 3])

    for start, stop, step in itr:
        assert slt[start:stop:step] == lst[start:stop:step]

@raises(ValueError)
def test_getitem_slicezero():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt[::0]

@raises(IndexError)
def test_getitem_indexerror1():
    slt = SortedListWithKey(key=negate)
    slt[5]

@raises(IndexError)
def test_getitem_indexerror2():
    slt = SortedListWithKey(range(100), key=negate)
    slt[200]

@raises(IndexError)
def test_getitem_indexerror3():
    slt = SortedListWithKey(range(100), key=negate)
    slt[-101]

def test_delitem():
    random.seed(0)
    slt = SortedListWithKey(range(100), load=17, key=negate)
    while len(slt) > 0:
        del slt[random.randrange(len(slt))]
        slt._check()

def test_delitem_slice():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    del slt[10:40:1]
    del slt[10:40:-1]
    del slt[10:40:2]
    del slt[10:40:-2]

def test_setitem():
    random.seed(0)
    slt = SortedListWithKey(range(0, 100, 10), load=4, key=negate)

    slt[-3] = 20
    slt._check()

    values = list(enumerate(range(95, 5, -10)))
    random.shuffle(values)
    for pos, val in values:
        slt[pos] = val

def test_setitem_slice():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt[:10] = iter(range(99, 89, -1))
    assert slt == list(range(99, -1, -1))
    slt[:10:2] = iter([99, 97, 95, 93, 91])
    assert slt == list(range(99, -1, -1))
    slt[-50:] = range(49, -51, -1)
    assert slt == list(range(99, -51, -1))
    slt[-100:] = range(49, -1, -1)
    assert slt == list(range(99, -1, -1))
    slt[:] = range(99, -1, -1)
    assert slt == list(range(99, -1, -1))
    slt[90:] = []
    assert slt == list(range(99, 9, -1))
    slt[:10] = []
    assert slt == list(range(89, 9, -1))

@raises(ValueError)
def test_setitem_slice_bad():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt[:10] = list(reversed(range(10)))

@raises(ValueError)
def test_setitem_slice_bad1():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt[10:20] = range(20, 30)

@raises(ValueError)
def test_setitem_slice_bad2():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt[20:30] = range(10, 20)

def test_setitem_extended_slice():
    slt = SortedListWithKey(range(1000, 0, -10), load=17, key=negate)
    lst = list(range(1000, 0, -10))
    lst[10:90:10] = range(905, 105, -100)
    slt[10:90:10] = range(905, 105, -100)
    assert slt == lst

@raises(ValueError)
def test_setitem_extended_slice_bad1():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt[20:80:3] = list(range(10))

@raises(ValueError)
def test_setitem_extended_slice_bad2():
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt[40:90:5] = list(range(10))

@raises(ValueError)
def test_setitem_valueerror1():
    slt = SortedListWithKey(range(10), key=negate)
    slt[9] = 10

@raises(ValueError)
def test_setitem_valueerror2():
    slt = SortedListWithKey(range(10), key=negate)
    slt[0] = 0

def test_iter():
    slt = SortedListWithKey(range(10000), key=negate)
    itr = iter(slt)
    assert all(tup[0] == tup[1] for tup in zip(range(9999, -1, -1), itr))

def test_reversed():
    slt = SortedListWithKey(range(10000), key=negate)
    rev = reversed(slt)
    assert all(tup[0] == tup[1] for tup in zip(range(10000), rev))

def test_islice():
    return
    slt = SortedListWithKey(load=7, key=negate)

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
    slt = SortedListWithKey(load=7, key=negate)

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
    slt = SortedListWithKey(key=negate)

    for val in range(10000):
        slt.add(val)
        assert len(slt) == (val + 1)

def test_bisect_left():
    slt = SortedListWithKey(key=negate)
    assert slt.bisect_left(0) == 0
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_left(50) == 98
    assert slt.bisect_left(0) == 198
    assert slt.bisect_left(-1) == 200

def test_bisect():
    slt = SortedListWithKey(key=negate)
    assert slt.bisect(10) == 0
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt.update(range(100))
    slt._check()
    assert slt.bisect(10) == 180
    assert slt.bisect(0) == 200

def test_bisect_right():
    slt = SortedListWithKey(key=negate)
    assert slt.bisect_right(10) == 0
    slt = SortedListWithKey(range(100), load=17, key=negate)
    slt.update(range(100))
    slt._check()
    assert slt.bisect_right(10) == 180
    assert slt.bisect_right(0) == 200

def test_copy():
    slt = SortedListWithKey(range(100), load=7, key=negate)
    two = slt.copy()
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_copy_copy():
    import copy
    slt = SortedListWithKey(range(100), load=7, key=negate)
    two = copy.copy(slt)
    slt.add(100)
    assert len(slt) == 101
    assert len(two) == 100

def test_count():
    slt = SortedListWithKey(load=7, key=negate)

    assert slt.count(0) == 0

    for iii in range(100):
        for jjj in range(iii):
            slt.add(iii)
        slt._check()

    for iii in range(100):
        assert slt.count(iii) == iii

def test_append():
    slt = SortedListWithKey(load=17, key=negate)

    slt.append(1000)

    for val in range(999, -1, -1):
        slt.append(val)
        slt._check()

@raises(ValueError)
def test_append_valueerror():
    slt = SortedListWithKey(range(100), key=negate)
    slt.append(5)

def test_extend():
    slt = SortedListWithKey(load=17, key=negate)

    slt.extend(range(300, 200, -1))
    slt._check()

    slt.extend(list(range(200, 100, -1)))
    slt._check()

    for val in range(100, 0, -1):
        del slt._index[:]
        slt._build_index()
        slt.extend([val] * (101 - val))
        slt._check()

@raises(ValueError)
def test_extend_valueerror1():
    slt = SortedListWithKey(key=negate)
    slt.extend([1, 2, 3, 5, 4, 6])

@raises(ValueError)
def test_extend_valueerror2():
    slt = SortedListWithKey(range(20), load=4, key=negate)
    slt.extend([5, 4, 3, 2, 1])

def test_insert():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.insert(-1, 0)
    slt._check()
    slt.insert(-100, 9)
    slt._check()
    slt.insert(0, 10)
    slt._check()
    slt.insert(14, -1)
    slt._check()

    slt = SortedListWithKey(load=4, key=negate)
    slt.insert(0, 5)
    slt._check()

    slt = SortedListWithKey(range(5, 15), load=4, key=negate)
    for rpt in range(8):
        slt.insert(0, 15)
        slt._check()

    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.insert(8, 2)
    slt._check()

@raises(ValueError)
def test_insert_valueerror1():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.insert(10, 5)

@raises(ValueError)
def test_insert_valueerror2():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.insert(0, 0)

@raises(ValueError)
def test_insert_valueerror3():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.insert(5, 3)

@raises(ValueError)
def test_insert_valueerror4():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.insert(5, 7)

def test_pop():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt._check()
    assert slt.pop() == 0
    slt._check()
    assert slt.pop(0) == 9
    slt._check()
    assert slt.pop(-2) == 2
    slt._check()
    assert slt.pop(4) == 4
    slt._check()

@raises(IndexError)
def test_pop_indexerror1():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.pop(-11)

@raises(IndexError)
def test_pop_indexerror2():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.pop(10)

def test_index():
    slt = SortedListWithKey(range(100), load=17, key=negate)

    for pos, val in enumerate(range(99, -1, -1)):
        assert val == slt.index(pos)

    assert slt.index(99, 0, 1000) == 0

    slt = SortedListWithKey((0 for rpt in range(100)), load=17, key=negate)

    for start in range(100):
        for stop in range(start, 100):
            assert slt.index(0, start, stop + 1) == start

    for start in range(100):
        assert slt.index(0, -(100 - start)) == start

    assert slt.index(0, -1000) == 0

@raises(ValueError)
def test_index_valueerror1():
    slt = SortedListWithKey([0] * 10, load=4, key=negate)
    slt.index(0, 10)

@raises(ValueError)
def test_index_valueerror2():
    slt = SortedListWithKey([0] * 10, load=4, key=negate)
    slt.index(0, 0, -10)

@raises(ValueError)
def test_index_valueerror3():
    slt = SortedListWithKey([0] * 10, load=4, key=negate)
    slt.index(0, 7, 3)

@raises(ValueError)
def test_index_valueerror4():
    slt = SortedListWithKey([0] * 10, load=4, key=negate)
    slt.index(1)

@raises(ValueError)
def test_index_valueerror5():
    slt = SortedListWithKey(key=negate)
    slt.index(1)

@raises(ValueError)
def test_index_valueerror6():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt.index(6, 5)

def test_mul():
    this = SortedListWithKey(range(10), load=4, key=negate)
    that = this * 5
    this._check()
    that._check()
    assert this == list(reversed((range(10))))
    assert that == list(sorted(list(range(10)) * 5, reverse=True))
    assert this != that

def test_imul():
    this = SortedListWithKey(range(10), load=4, key=negate)
    this *= 5
    this._check()
    assert this == sorted(list(range(10)) * 5, reverse=True)

def test_op_add():
    this = SortedListWithKey(range(10), load=4, key=negate)
    assert (this + this + this) == (this * 3)

    that = SortedListWithKey(range(10), load=4, key=negate)
    that += that
    that += that
    assert that == (this * 4)

def test_eq():
    this = SortedListWithKey(range(10), load=4, key=negate)
    that = SortedListWithKey(range(20), load=4, key=negate)
    assert not (this == that)
    that.clear()
    that.update(range(10))
    assert this == that

def test_lt():
    this = SortedListWithKey(range(10), load=4, key=negate)
    that = SortedListWithKey(range(10, 20), load=5, key=negate)
    assert this < that
    assert not (that < this)
    that = SortedListWithKey(range(1, 20), load=6, key=negate)
    assert this < that
    that = SortedListWithKey(range(1, 10), load=4, key=negate)
    assert not (this < that)

def test_lte():
    this = SortedListWithKey(range(10), load=4, key=negate)
    that = SortedListWithKey(range(10), load=5, key=negate)
    assert this <= that
    assert that <= this
    del this[-1]
    assert this <= that
    assert not (that <= this)

def test_gt():
    this = SortedListWithKey(range(10), load=4, key=negate)
    that = SortedListWithKey(range(10, 20), load=5, key=negate)
    assert that > this
    assert not (this > that)
    that = SortedListWithKey(range(1, 20), load=6, key=negate)
    assert that > this
    that = SortedListWithKey(range(1, 10), load=4, key=negate)
    assert not (that > this)

def test_gte():
    this = SortedListWithKey(range(10), load=4, key=negate)
    that = SortedListWithKey(range(10), load=5, key=negate)
    assert this >= that
    assert that >= this
    del this[-1]
    assert that >= this
    assert not (this >= that)

def test_repr():
    this = SortedListWithKey(range(10), load=4, key=negate)
    assert repr(this).startswith('SortedListWithKey([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], key=<function negate at ')

def test_pickle():
    import pickle
    alpha = SortedListWithKey(range(10000), key=negate, load=500)
    beta = pickle.loads(pickle.dumps(alpha))
    assert alpha == beta
    assert alpha._key == beta._key
    assert alpha._load == beta._load

@raises(AssertionError)
def test_check():
    slt = SortedListWithKey(range(10), load=4, key=negate)
    slt._len = 5
    slt._check()

if __name__ == '__main__':
    import nose
    nose.main()
