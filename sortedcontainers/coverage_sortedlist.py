# -*- coding: utf-8 -*-

import random
from sortedlist import SortedList
from nose.tools import raises

def test_init():
    slt = SortedList()
    slt._check()

    slt = SortedList(load=10000)
    assert slt._load == 10000
    assert slt._twice == 20000
    assert slt._half == 5000
    slt._check()

    slt = SortedList(xrange(10000))
    assert all(tup[0] == tup[1] for tup in zip(slt, list(xrange(10000))))

    slt.clear()
    assert slt._len == 0
    assert slt._maxes == None
    assert slt._lists == None
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
    assert all(tup[0] == tup[1] for tup in zip(slt, list(xrange(1000))))
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

    assert all(tup[0] == tup[1] for tup in zip(slt, [1, 2, 2, 3, 3, 5]))

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

    assert all(tup[0] == tup[1] for tup in zip(slt, [1, 2, 2, 3, 3, 5]))

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
    assert slt._lists == None

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

@raises(IndexError)
def test_getitem_indexerror1():
    slt = SortedList()
    print slt[5]

@raises(IndexError)
def test_getitem_indexerror2():
    slt = SortedList(xrange(100))
    print slt[200]

def test_delitem():
    random.seed(0)
    slt = SortedList(xrange(100), load=17)
    while len(slt) > 0:
        del slt[random.randrange(len(slt))]
        slt._check()

def test_setitem():
    random.seed(0)
    slt = SortedList(xrange(0, 100, 10), load=4)

    values = list(enumerate(xrange(5, 105, 10)))
    random.shuffle(values)
    for pos, val in values:
        slt[pos] = val

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
    assert all(tup[0] == tup[1] for tup in zip(xrange(10000), itr))

def test_reversed():
    slt = SortedList(xrange(10000))
    rev = slt.reversed()
    assert all(tup[0] == tup[1] for tup in zip(xrange(9999, -1, -1), rev))

def test_len():
    slt = SortedList()

    for val in xrange(10000):
        slt.add(val)
        assert len(slt) == (val + 1)

def test_bisect_left():
    slt = SortedList(xrange(10000))
    slt.update(xrange(10000))
    slt._check()
    assert slt.bisect_left(1000) == 2000

def test_bisect():
    test_bisect_left()

def test_bisect_right():
    slt = SortedList(xrange(10000))
    slt.update(xrange(10000))
    slt._check()
    assert slt.bisect_right(1000) == 2002

def test_count():
    slt = SortedList(load=7)

    assert slt.count(0) == 0

    for iii in xrange(100):
        for jjj in xrange(iii):
            slt.add(iii)
        slt._check()

    for iii in xrange(100):
        print slt.count(iii), iii
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
def test_insert_valueerror2():
    slt = SortedList(xrange(10), load=4)
    slt.insert(0, 10)

@raises(ValueError)
def test_insert_valueerror3():
    slt = SortedList(xrange(10), load=4)
    slt.insert(5, 3)

@raises(ValueError)
def test_insert_valueerror3():
    slt = SortedList(xrange(10), load=4)
    slt.insert(5, 7)

def test_pop():
    slt = SortedList(xrange(10), load=4)
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

