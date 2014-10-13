# -*- coding: utf-8 -*-

from __future__ import print_function
from sys import hexversion

import random
from .context import sortedcontainers
from sortedcontainers import SortedDict
from nose.tools import raises
from functools import wraps

if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

random.seed(0)
actions = []

def actor(func):
    actions.append(func)
    return func

def test_init():
    sdict = SortedDict()
    sdict._check()

    sdict = SortedDict(load=17)
    sdict._check()

    sdict = SortedDict((val, -val) for val in range(10000))
    sdict._check()
    assert all(key == -val for key, val in sdict.iteritems())

    sdict.clear()
    sdict._check()
    assert len(sdict) == 0

    sdict = SortedDict.fromkeys(range(1000), None)
    assert all(sdict[key] == None for key in range(1000))

@actor
def stress_contains(sdict):
    keys = list(sdict)
    assert all((key in sdict for key in keys))

@actor
def stress_delitem(sdict):
    keys = list(sdict)
    for rpt in range(100):
        pos = random.randrange(0, len(sdict))
        del sdict[keys[pos]]
        del keys[pos]

@actor
def stress_getitem(sdict):
    items = list(sdict.iteritems())
    assert all(sdict[key] == value for key, value in items)
    
@actor
def stress_eq(sdict):
    that = dict((key, value) for key, value in sdict.iteritems())
    assert sdict == that

@actor
def stress_setitem_len(sdict):
    start_len = len(sdict)
    keys = list(range(100))
    missing = sum(1 for val in keys if val not in sdict)
    for val in keys:
        sdict[val] = -val
    end_len = len(sdict)
    assert (start_len + missing) == end_len

@actor
def stress_copy(sdict):
    that = sdict.copy()

@actor
def stress_get(sdict):
    keys = list(range(100))
    for key in keys:
        if key in sdict:
            assert sdict.get(key, 1) == -key
        else:
            assert sdict.get(key, 1) == 1

@actor
def stress_has_key(sdict):
    if hexversion > 0x03000000:
        return
    keys = list(range(100))
    for key in keys:
        assert all((key in sdict) == (sdict.has_key(key)) for key in sdict)

@actor
def stress_items_keys_values(sdict):
    items = sdict.items()
    keys = sdict.keys()
    values = sdict.values()
    assert list(items) == list(zip(keys, values))

@actor
def stress_iter_items_keys_values(sdict):
    it = zip(sdict.iteritems(), sdict.iterkeys(), sdict.itervalues())
    assert all(tup[0] == (tup[1], tup[2]) for tup in it)

@actor
def stress_pop(sdict):
    keys = list(range(200))
    for key in keys:
        if key in sdict:
            val = sdict[key]
            assert sdict.pop(key, 1) == val
        else:
            assert sdict.pop(key, 1) == 1

@actor
def stress_popitem(sdict):
    items = [sdict.popitem() for rpt in range(100)]
    keys = [item[0] for item in items]
    assert all(keys[pos - 1] > keys[pos] for pos in range(1, len(keys)))
    assert all(key == -value for key, value in items)

@actor
def stress_setdefault(sdict):
    keys = list(range(200))
    for key in keys:
        if key in sdict:
            assert sdict.setdefault(key) == -key
        else:
            sdict.setdefault(key)
            assert sdict[key] == None
            del sdict[key]

def test_stress(repeat=1000):
    sdict = SortedDict((val, -val) for val in range(1000))

    for rpt in range(repeat):
        action = random.choice(actions)
        action(sdict)

        try:
            sdict._check()
        except AssertionError:
            print(action)
            raise

        start_len = len(sdict)

        while len(sdict) < 500:
            key = random.randrange(0, 2000)
            sdict[key] = -key

        while len(sdict) > 2000:
            key = random.randrange(0, 2000)
            if key in sdict:
                del sdict[key]

        if start_len != len(sdict):
            sdict._check()

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
