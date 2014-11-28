# -*- coding: utf-8 -*-

from __future__ import print_function
from sys import hexversion

import copy
import bisect
import random
from .context import sortedcontainers
from sortedcontainers import SortedListWithKey
from nose.tools import raises
from functools import wraps

class SortedList(SortedListWithKey):
    pass

if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

random.seed(0)
actions = []

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

class actor:
    def __init__(self, count):
        self._count = count
    def __call__(self, func):
        actions.extend([func] * self._count)
        return func

def not_empty(func):
    @wraps(func)
    def wrapper(slt):
        if len(slt) < 100:
            stress_update(slt)
        func(slt)
    return wrapper

@actor(1)
def stress_clear(slt):
    if random.randrange(100) < 10:
        slt.clear()
    else:
        values = list(slt)
        slt.clear()
        slt.update(values[:int(len(values) / 2)])

@actor(1)
def stress_add(slt):
    if random.randrange(100) < 10:
        slt.clear()
    slt.add(random.random())

@actor(1)
def stress_update(slt):
    slt.update((random.random() for rpt in range(350)))

@actor(1)
@not_empty
def stress_contains(slt):
    if random.randrange(100) < 10:
        slt.clear()
        assert 0 not in slt
    else:
        val = slt[random.randrange(len(slt))]
        assert val in slt
        assert 1 not in slt

@actor(1)
@not_empty
def stress_discard(slt):
    val = slt[random.randrange(len(slt))]
    slt.discard(val)

@actor(1)
def stress_discard2(slt):
    if random.randrange(100) < 10:
        slt.clear()
    slt.discard(random.random())

@actor(1)
def stress_remove(slt):
    if len(slt) > 0:
        val = slt[random.randrange(len(slt))]
        slt.remove(val)

    try:
        slt.remove(1)
        assert False
    except ValueError:
        pass

    try:
        slt.remove(-1)
        assert False
    except ValueError:
        pass

@actor(1)
@not_empty
def stress_delitem(slt):
    del slt[random.randrange(len(slt))]

@actor(1)
def stress_getitem(slt):
    if len(slt) > 0:
        pos = random.randrange(len(slt))
        assert slt[pos] == list(slt)[pos]

        try:
            slt[-(slt._len + 5)]
            assert False
        except IndexError:
            pass

        try:
            slt[slt._len + 5]
            assert False
        except IndexError:
            pass
    else:
        try:
            slt[0]
            assert False
        except IndexError:
            pass

@actor(1)
@not_empty
def stress_setitem(slt):
    pos = random.randrange(len(slt))
    slt[pos] = slt[pos]

@actor(1)
@not_empty
def stress_setitem2(slt):
    pos = random.randrange(int(len(slt) / 100)) * 100
    slt[pos] = slt[pos]

@actor(1)
@not_empty
def stress_getset_slice(slt):
    start, stop = sorted(random.randrange(len(slt)) for rpt in range(2))
    step = random.choice([-3, -2, -1, 1, 1, 1, 1, 1, 2, 3])
    lst = slt[start:stop:step]
    assert all(lst[pos - 1] <= lst[pos] for pos in range(1, len(lst)))
    slt[start:stop:step] = lst

@actor(1)
@not_empty
def stress_delitem_slice(slt):
    start, stop = sorted(random.randrange(len(slt)) for rpt in range(2))
    step = random.choice([-3, -2, -1, 1, 1, 1, 1, 1, 2, 3])
    del slt[start:stop:step]

@actor(1)
def stress_iter(slt):
    itr1 = iter(slt)
    itr2 = (slt[pos] for pos in range(len(slt)))
    assert all(tup[0] == tup[1] for tup in zip(itr1, itr2))

@actor(1)
def stress_reversed(slt):
    itr = reversed(list(reversed(slt)))
    assert all(tup[0] == tup[1] for tup in zip(slt, itr))

@actor(1)
def stress_bisect_left(slt):
    values = list(slt)
    value = random.random()
    values.sort()
    assert bisect.bisect_left(values, value) == slt.bisect_left(value)

@actor(1)
def stress_bisect(slt):
    values = list(slt)
    value = random.random()
    values.sort()
    assert bisect.bisect(values, value) == slt.bisect(value)

@actor(1)
def stress_bisect_right(slt):
    values = list(slt)
    value = random.random()
    values.sort()
    assert bisect.bisect_right(values, value) == slt.bisect_right(value)

@actor(1)
@not_empty
def stress_dups(slt):
    pos = min(random.randrange(len(slt)), 300)
    val = slt[pos]
    for rpt in range(pos):
        slt.add(val)

@actor(1)
@not_empty
def stress_count(slt):
    values = list(slt)
    val = slt[random.randrange(len(slt))]
    assert slt.count(val) == values.count(val)

@actor(1)
def stress_append(slt):
    if random.randrange(100) < 10:
        slt.clear()
    if len(slt) == 0:
        slt.append(random.random())
    else:
        slt.append(slt[-1])

@actor(1)
def stress_extend(slt):
    if random.randrange(100) < 10:
        slt.clear()
    if len(slt) == 0:
        slt.extend(float(val) / 1000 for val in range(1000))
    else:
        slt.extend(frange(slt[-1], 1, 0.001))

@actor(1)
@not_empty
def stress_insert(slt):
    slt.insert(0, slt[0])
    slt.insert(-(len(slt) + 10), slt[0])

    slt.insert(len(slt), slt[-1])
    slt.insert(len(slt) + 10, slt[-1])

    pos = random.randrange(len(slt))
    slt.insert(pos, slt[pos])

@actor(1)
def stress_insert2(slt):
    if random.randrange(100) < 10:
        slt.clear()
    if len(slt) == 0:
        slt.insert(0, random.random())
    else:
        values = list(slt)[:250]
        for val in values:
            slt.insert(slt.index(val), val)

@actor(1)
@not_empty
def stress_pop(slt):
    pos = random.randrange(len(slt)) + 1
    assert slt[-pos] == slt.pop(-pos)

@actor(1)
@not_empty
def stress_index(slt):
    values = set(slt)
    slt.clear()
    slt.update(values)
    pos = random.randrange(len(slt))
    assert slt.index(slt[pos]) == pos

@actor(1)
@not_empty
def stress_index2(slt):
    values = list(slt)[:3] * 200
    slt = SortedList(values)
    for idx, val in enumerate(slt):
        assert slt.index(val, idx) == idx

@actor(1)
def stress_mul(slt):
    values = list(slt)
    mult = random.randrange(10)
    values *= mult
    values.sort()
    assert (slt * mult) == values

@actor(1)
def stress_imul(slt):
    mult = random.randrange(10)
    slt *= mult

@actor(1)
@not_empty
def stress_reversed(slt):
    itr = reversed(slt)
    pos = random.randrange(1, len(slt))
    for rpt in range(pos):
        val = next(itr)
    assert val == slt[-pos]

@actor(1)
@not_empty
def stress_eq(slt):
    values = []
    assert not (values == slt)

@actor(1) # Disabled!!!
@not_empty
def stress_lt(slt):
    values = list(slt) # Doesn't work with nose!
    assert not (values < slt)
    values = SortedList(value - 1 for value in values)
    assert values < slt
    values = []
    assert values < slt
    assert not (slt < values)

def test_stress(repeat=1000):
    slt = SortedList((random.random() for rpt in range(1000)))

    for rpt in range(repeat):
        action = random.choice(actions)
        action(slt)

        slt._check()

        while len(slt) > 2000:
            # Shorten the sortedlist. This maintains the "jaggedness"
            # of the sublists which helps coverage.
            pos = random.randrange(len(slt._maxes))
            del slt._maxes[pos]
            del slt._keys[pos]
            del slt._lists[pos]
            slt._len = sum(len(sublist) for sublist in slt._lists)
            slt._index = []
            slt._check()

    slt._check()

    stress_update(slt)

    while len(slt) > 0:
        pos = random.randrange(len(slt))
        del slt[pos]

    slt._check()

if __name__ == '__main__':
    import sys
    from datetime import datetime

    start = datetime.now()

    print('Python', sys.version_info)

    try:
        num = int(sys.argv[1])
        print('Setting iterations to', num)
    except:
        print('Setting iterations to 1000 (default)')
        num = 1000

    try:
        pea = int(sys.argv[2])
        random.seed(pea)
        print('Setting seed to', pea)
    except:
        print('Setting seed to 0 (default)')
        random.seed(0)

    try:
        test_stress(num)
    except:
        raise
    finally:
        print('Exiting after', (datetime.now() - start))
