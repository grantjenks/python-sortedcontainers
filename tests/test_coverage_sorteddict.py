# -*- coding: utf-8 -*-

import random, string
from .context import sortedcontainers
from sortedcontainers import SortedDict
import pytest
from sys import hexversion

if hexversion < 0x03000000:
    range = xrange

def negate(value):
    return -value

def modulo(value):
    return value % 10

def get_keysview(dic):
    if hexversion < 0x03000000:
        return dic.viewkeys()
    else:
        return dic.keys()

def get_itemsview(dic):
    if hexversion < 0x03000000:
        return dic.viewitems()
    else:
        return dic.items()

def test_init():
    temp = SortedDict()
    assert temp.key is None
    temp._check()

def test_init_key():
    temp = SortedDict(negate)
    assert temp.key == negate
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
    assert list(temp.items()) == mapping
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
    assert not (temp1 != temp2)
    temp2['a'] = 100
    assert temp1 != temp2
    assert not (temp1 == temp2)
    del temp2['a']
    assert temp1 != temp2
    assert not (temp1 == temp2)
    temp2['zz'] = 0
    assert temp1 != temp2
    assert not (temp1 == temp2)

def test_iter():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all(lhs == rhs for lhs, rhs in zip(temp, string.ascii_lowercase))

def test_iter_key():
    temp = SortedDict(negate, ((val, val) for val in range(100)))
    temp._reset(7)
    assert all(lhs == rhs for lhs, rhs in zip(temp, reversed(range(100))))

def test_reversed():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all(lhs == rhs for lhs, rhs in
               zip(reversed(temp), reversed(string.ascii_lowercase)))

def test_reversed_key():
    temp = SortedDict(modulo, ((val, val) for val in range(100)))
    temp._reset(7)
    values = sorted(range(100), key=modulo)
    assert all(lhs == rhs for lhs, rhs in zip(reversed(temp), reversed(values)))

def test_islice():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    temp._reset(7)

    for start in range(30):
        for stop in range(30):
            assert list(temp.islice(start, stop)) == list(string.ascii_lowercase[start:stop])

def test_irange():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    temp._reset(7)
    for start in range(26):
        for stop in range(start + 1, 26):
            result = list(string.ascii_lowercase[start:stop])
            assert list(temp.irange(result[0], result[-1])) == result

def test_irange_key():
    temp = SortedDict(modulo, ((val, val) for val in range(100)))
    temp._reset(7)
    values = sorted(range(100), key=modulo)

    for start in range(10):
        for stop in range(start, 10):
            result = list(temp.irange_key(start, stop))
            assert result == values[(start * 10):((stop + 1) * 10)]

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
    assert len(dup) == 26
    dup.clear()
    assert len(temp) == 26
    assert len(dup) == 0

def test_copy_copy():
    import copy
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    dup = copy.copy(temp)
    assert len(temp) == 26
    assert len(dup) == 26
    dup.clear()
    assert len(temp) == 26
    assert len(dup) == 0

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
    if hexversion > 0x03000000:
        return
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.has_key('a')

def test_items():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert list(temp.items()) == mapping

def test_keys():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert list(temp.keys()) == [key for key, pos in mapping]

def test_values():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert list(temp.values()) == [pos for key, pos in mapping]

def test_notgiven():
    assert repr(SortedDict._SortedDict__not_given) == '<not-given>'

def test_pop():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.pop('a') == 0
    assert temp.pop('a', -1) == -1

def test_pop2():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    with pytest.raises(KeyError):
        temp.pop('A')

def test_popitem():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.popitem() == ('z', 25)

def test_popitem2():
    temp = SortedDict()
    with pytest.raises(KeyError):
        temp.popitem()

def test_popitem3():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.popitem(index=0) == ('a', 0)

def test_peekitem():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.peekitem() == ('z', 25)
    assert temp.peekitem(0) == ('a', 0)
    assert temp.peekitem(index=4) == ('e', 4)

def test_peekitem2():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    with pytest.raises(IndexError):
        temp.peekitem(index=100)

def test_setdefault():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.setdefault('a', -1) == 0
    assert temp['a'] == 0
    assert temp.setdefault('A', -1) == -1

def test_update():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict()
    temp.update()
    temp.update(mapping)
    temp.update(dict(mapping))
    temp.update(mapping[5:7])
    assert list(temp.items()) == mapping

def test_update2():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict()
    temp.update(**dict(mapping))
    assert list(temp.items()) == mapping

def test_repr():
    temp = SortedDict({'alice': 3, 'bob': 1, 'carol': 2, 'dave': 4})
    assert repr(temp) == "SortedDict({'alice': 3, 'bob': 1, 'carol': 2, 'dave': 4})"

class Identity(object):
    def __call__(self, value):
        return value
    def __repr__(self):
        return 'identity'

def test_repr_recursion():
    temp = SortedDict(Identity(), {'alice': 3, 'bob': 1, 'carol': 2, 'dave': 4})
    temp['bob'] = temp
    assert repr(temp) == "SortedDict(identity, {'alice': 3, 'bob': ..., 'carol': 2, 'dave': 4})"

def test_repr_subclass():
    class CustomSortedDict(SortedDict):
        pass
    temp = CustomSortedDict({'alice': 3, 'bob': 1, 'carol': 2, 'dave': 4})
    assert repr(temp) == "CustomSortedDict({'alice': 3, 'bob': 1, 'carol': 2, 'dave': 4})"

def test_index():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.index('a') == 0
    assert temp.index('f', 3, -3) == 5

def test_iloc():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert len(temp.iloc) == 26
    assert temp.iloc[0] == 'a'
    assert temp.iloc[-1] == 'z'
    assert temp.iloc[-3:] == ['x', 'y', 'z']
    del temp.iloc[0]
    assert temp.iloc[0] == 'b'
    del temp.iloc[-3:]
    assert temp.iloc[-1] == 'w'

def test_index_key():
    temp = SortedDict(negate, ((val, val) for val in range(100)))
    temp._reset(7)
    assert all(temp.index(val) == (99 - val) for val in range(100))

def test_bisect():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert temp.bisect_left('a') == 0
    assert temp.bisect_right('f') == 6
    assert temp.bisect('f') == 6

def test_bisect_key():
    temp = SortedDict(modulo, ((val, val) for val in range(100)))
    temp._reset(7)
    assert all(temp.bisect(val) == ((val % 10) + 1) * 10 for val in range(100))
    assert all(temp.bisect_right(val) == ((val % 10) + 1) * 10 for val in range(100))
    assert all(temp.bisect_left(val) == (val % 10) * 10 for val in range(100))

def test_bisect_key2():
    temp = SortedDict(modulo, ((val, val) for val in range(100)))
    temp._reset(7)
    assert all(temp.bisect_key(val) == ((val % 10) + 1) * 10 for val in range(10))
    assert all(temp.bisect_key_right(val) == ((val % 10) + 1) * 10 for val in range(10))
    assert all(temp.bisect_key_left(val) == (val % 10) * 10 for val in range(10))

def test_keysview():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    keys = temp.keys()

    assert len(keys) == 13
    assert 'a' in keys
    assert list(keys) == [val for val, pos in mapping[:13]]
    assert keys[0] == 'a'
    assert list(reversed(keys)) == list(reversed(string.ascii_lowercase[:13]))
    assert keys.index('f') == 5
    assert keys.count('m') == 1
    assert keys.count('0') == 0
    assert keys.isdisjoint(['1', '2', '3'])

    temp.update(mapping[13:])

    assert len(keys) == 26
    assert 'z' in keys
    assert list(keys) == [val for val, pos in mapping]

    that = dict(mapping)

    that_keys = get_keysview(that)

    assert keys == that_keys
    assert not (keys != that_keys)
    assert not (keys < that_keys)
    assert not (keys > that_keys)
    assert keys <= that_keys
    assert keys >= that_keys

    assert sorted(keys & that_keys) == [val for val, pos in mapping]
    assert sorted(keys | that_keys) == [val for val, pos in mapping]
    assert sorted(keys - that_keys) == []
    assert sorted(keys ^ that_keys) == []

    keys = SortedDict(mapping[:2]).keys()
    assert repr(keys) == "SortedKeysView(SortedDict({'a': 0, 'b': 1}))"

def test_valuesview():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    values = temp.values()

    assert len(values) == 13
    assert 0 in values
    assert list(values) == [pos for val, pos in mapping[:13]]
    assert values[0] == 0
    assert values[-3:] == [10, 11, 12]
    assert list(reversed(values)) == list(reversed(range(13)))
    assert values.index(5) == 5
    assert values.count(10) == 1

    temp.update(mapping[13:])

    assert len(values) == 26
    assert 25 in values
    assert list(values) == [pos for val, pos in mapping]

    values = SortedDict(mapping[:2]).values()
    assert repr(values) == "SortedValuesView(SortedDict({'a': 0, 'b': 1}))"

def test_values_view_index():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    values = temp.values()
    with pytest.raises(ValueError):
        values.index(100)

def test_itemsview():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    items = temp.items()

    assert len(items) == 13
    assert ('a', 0) in items
    assert list(items) == mapping[:13]
    assert items[0] == ('a', 0)
    assert items[-3:] == [('k', 10), ('l', 11), ('m', 12)]
    assert list(reversed(items)) == list(reversed(mapping[:13]))
    assert items.index(('f', 5)) == 5
    assert items.count(('m', 12)) == 1
    assert items.isdisjoint([('0', 26), ('1', 27)])
    assert not items.isdisjoint([('a', 0), ('b', 1)])

    temp.update(mapping[13:])

    assert len(items) == 26
    assert ('z', 25) in items
    assert list(items) == mapping

    that = dict(mapping)
    that_items = get_itemsview(that)

    assert items == that_items
    assert not (items != that_items)
    assert not (items < that_items)
    assert not (items > that_items)
    assert items <= that_items
    assert items >= that_items

    assert sorted(items & that_items) == mapping
    assert sorted(items | that_items) == mapping
    assert sorted(items - that_items) == []
    assert sorted(items ^ that_items) == []

    items = SortedDict(mapping[:2]).items()
    assert repr(items) == "SortedItemsView(SortedDict({'a': 0, 'b': 1}))"

def test_items_view_index():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping[:13])
    items = temp.items()
    with pytest.raises(ValueError):
        items.index(('f', 100))

def test_pickle():
    import pickle
    alpha = SortedDict(negate, zip(range(10000), range(10000)))
    alpha._reset(500)
    beta = pickle.loads(pickle.dumps(alpha))
    assert alpha == beta
    assert alpha._key == beta._key
