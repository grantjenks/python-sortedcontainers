# -*- coding: utf-8 -*-

import random, string
from context import sortedcontainers
from sortedcontainers import SortedDict
from nose.tools import raises

def test_init():
    temp = SortedDict()
    temp._check()

def test_init_args():
    temp = SortedDict([('a', 1), ('b', 2)])
    assert len(temp) == 2
    assert temp['a'] == 1
    assert temp['b'] == 2
    temp._check()

def test_init_kwargs():
    temp = SortedDict(a=1, b=2)
    assert len(temp) == 2
    assert temp['a'] == 1
    assert temp['b'] == 2
    temp._check()

def test_clear():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert len(temp) == 26
    assert temp.items() == mapping
    temp.clear()
    assert len(temp) == 0

def test_contains():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all((val in temp) for val in string.ascii_lowercase)

def test_delitem():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    del temp['a']
    temp._check()

def test_getitem():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all((temp[val] == pos) for pos, val in enumerate(string.ascii_lowercase))

def test_eq():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp1 = SortedDict(mapping)
    temp2 = SortedDict(mapping)
    assert temp1 == temp2

def test_iter():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all(lhs == rhs for lhs, rhs in zip(temp, string.ascii_lowercase))

def test_len():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert len(temp) == 26

def test_setitem():
    temp = SortedDict()

    for pos, key in enumerate(string.ascii_lowercase):
        temp[key] = pos
        temp._check()

    assert len(temp) == 26

    for pos, key in enumerate(string.ascii_lowercase):
        temp[key] = pos
        temp._check()

    assert len(temp) == 26

def test_copy():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    dup = temp.copy()
    assert len(temp) == 26
    dup.clear()
    assert len(temp) == 0

def test_fromkeys():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict.fromkeys(mapping, 1)
    assert all(temp[key] == 1 for key in temp)

def test_get():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.get('a') == 0
    assert temp.get('A', -1) == -1

def test_has_key():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.has_key('a')

def test_items():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.items() == mapping

def test_iteritems():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert list(temp.iteritems()) == mapping

def test_keys():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.keys() == [key for key, pos in mapping]

def test_iterkeys():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert list(temp.iterkeys()) == [key for key, pos in mapping]

def test_values():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.values() == [pos for key, pos in mapping]

def test_itervalues():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert list(temp.itervalues()) == [pos for key, pos in mapping]

def test_pop():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.pop('a') == 0
    assert temp.pop('a', -1) == -1

@raises(KeyError)
def test_pop2():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    temp.pop('A')

def test_popitem():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.popitem() == ('z', 25)

def test_setdefault():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.setdefault('a', -1) == 0
    assert temp['a'] == 0
    assert temp.setdefault('A', -1) == -1

def test_update():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict()
    temp.update(mapping)
    assert temp.items() == mapping

def test_update2():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict()
    temp.update(**dict(mapping))
    assert temp.items() == mapping

def test_keysview():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    keys = temp.viewkeys()

    assert len(keys) == 13
    assert 'a' in keys
    assert list(keys) == [val for val, pos in mapping[:13]]

    temp.update(mapping[13:])

    assert len(keys) == 26
    assert 'z' in keys
    assert list(keys) == [val for val, pos in mapping]

    that = dict(mapping)

    that_keys = that.viewkeys()

    assert keys == that_keys
    assert not (keys != that_keys)
    assert not (keys < that_keys)
    assert not (keys > that_keys)
    assert keys <= that_keys
    assert keys >= that_keys

    assert list(keys & that_keys) == [val for val, pos in mapping]
    assert list(keys | that_keys) == [val for val, pos in mapping]
    assert list(keys - that_keys) == []
    assert list(keys ^ that_keys) == []

    keys = SortedDict(mapping[:2]).viewkeys()
    assert repr(keys) == "SortedDict_keys(['a', 'b'])"

def test_valuesview():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    values = temp.viewvalues()

    assert len(values) == 13
    assert 0 in values
    assert list(values) == [pos for val, pos in mapping[:13]]

    temp.update(mapping[13:])

    assert len(values) == 26
    assert 25 in values
    assert list(values) == [pos for val, pos in mapping]

    values = SortedDict(mapping[:2]).viewvalues()
    assert repr(values) == "SortedDict_values([0, 1])"

@raises(TypeError)
def test_values_view_lt():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values < that_values

@raises(TypeError)
def test_values_view_gt():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values > that_values

@raises(TypeError)
def test_values_view_lte():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values <= that_values

@raises(TypeError)
def test_values_view_gte():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values >= that_values

@raises(TypeError)
def test_values_view_and():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values & that_values

@raises(TypeError)
def test_values_view_or():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values | that_values

@raises(TypeError)
def test_values_view_sub():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values - that_values

@raises(TypeError)
def test_values_view_xor():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    values = temp.viewvalues()
    that = dict(mapping)
    that_values = that.viewvalues()
    values ^ that_values

def test_itemsview():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    items = temp.viewitems()

    assert len(items) == 13
    assert ('a', 0) in items
    assert list(items) == mapping[:13]

    temp.update(mapping[13:])

    assert len(items) == 26
    assert ('z', 25) in items
    assert list(items) == mapping

    that = dict(mapping)

    that_items = that.viewitems()

    assert items == that_items
    assert not (items != that_items)
    assert not (items < that_items)
    assert not (items > that_items)
    assert items <= that_items
    assert items >= that_items

    assert list(items & that_items) == mapping
    assert list(items | that_items) == mapping
    assert list(items - that_items) == []
    assert list(items ^ that_items) == []

    items = SortedDict(mapping[:2]).viewitems()
    assert repr(items) == "SortedDict_items([('a', 0), ('b', 1)])"

if __name__ == '__main__':
    import nose
    nose.main()
