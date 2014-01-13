# -*- coding: utf-8 -*-

import random
from context import sortedcontainers
from sortedcontainers import SortedDict
from nose.tools import raises
from functools import wraps
from itertools import izip

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

    sdict = SortedDict(xrange(10000))
    sdict._check()
    assert all(tup[0] == tup[1] for tup in izip(sdict, xrange(10000)))

    sdict.clear()
    sdict._check()
    assert len(sst) == 0

    sdict = SortedDict.fromkeys(xrange(1000), None)
    assert all(sdict[key] == None for key in xrange(1000))

@actor
def stress_contains(sdict):
    keys = list(sdict)
    assert all((key in sdict for key in keys))

@actor
def stress_delitem(sdict):
    keys = list(sdict)
    for rpt in xrange(100):
        pos = random.randrange(0, len(sdict))
        del sdict[keys[pos]]
        del keys[pos]

@actor
def stress_getitem(sdict):
    items = list(sdict.iteritems())
    assert all(sdict[key] == value for key, value in items)
    
@actor
def stress_eq(sdict):
    that = {key: value for key, value in sdict.iteritems()}
    assert sdict == that

@actor
def stress_setitem_len(sdict):
    start_len = len(sdict)
    keys = list(xrange(100))
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
    keys = list(xrange(100))
    for key in keys:
        if key in sdict:
            assert sdict.get(key, 1) == -key
        else:
            assert sdict.get(key, 1) == 1

@actor
def stress_has_key(sdict):
    keys = list(xrange(100))
    for key in keys:
        assert all((key in sdict) == (sdict.has_key(key)) for key in sdict)

@actor
def stress_items_keys_values(sdict):
    items = sdict.items()
    keys = sdict.keys()
    values = sdict.values()
    assert items == zip(keys, values)

@actor
def stress_iter_items_keys_values(sdict):
    it = izip(sdict.iteritems(), sdict.iterkeys(), sdict.itervalues())
    assert all(tup[0] == (tup[1], tup[2]) for tup in it)

@actor
def stress_pop(sdict):
    keys = list(xrange(200))
    for key in keys:
        if key in sdict:
            val = sdict[key]
            assert sdict.pop(key, 1) == val
        else:
            assert sdict.pop(key, 1) == 1

@actor
def stress_popitem(sdict):
    items = [sdict.popitem() for rpt in xrange(100)]
    keys = [item[0] for item in items]
    assert all(keys[pos - 1] > keys[pos] for pos in xrange(1, len(keys)))
    assert all(key == -value for key, value in items)

@actor
def stress_setdefault(sdict):
    keys = list(xrange(200))
    for key in keys:
        if key in sdict:
            assert sdict.setdefault(key) == -key
        else:
            sdict.setdefault(key)
            assert sdict[key] == None
            del sdict[key]

@actor
def stress_update(sdict):
    sdict.update((val, -val) for val in xrange(100))
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    sdict.update(**{val: val for val in letters})
    for letter in letters:
        del sdict[letter]

def test_stress(repeat=1000):
    sdict = SortedDict((val, -val) for val in xrange(1000))

    for rpt in xrange(repeat):
        action = random.choice(actions)
        action(sdict)

        try:
            sdict._check()
        except AssertionError:
            print action
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

    try:
        num = int(sys.argv[1])
        print 'Setting iterations to', num
    except:
        print 'Setting iterations to 1000 (default)'
        num = 1000

    try:
        pea = int(sys.argv[2])
        random.seed(pea)
        print 'Setting seed to', pea
    except:
        print 'Setting seed to 0 (default)'
        random.seed(0)

    try:
        test_stress(num)
    except:
        raise
    finally:
        print 'Exiting after', (datetime.now() - start)
