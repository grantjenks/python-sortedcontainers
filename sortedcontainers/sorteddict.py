"""
Sorted dict implementation.
"""

from .sortedset import SortedSet
from .sortedlist import SortedList
from collections import MutableMapping

from sys import version_info, hexversion

_NotGiven = object()

def not26(func):
    from functools import wraps

    @wraps(func)
    def errfunc(*args, **kwargs):
        raise NotImplementedError

    if hexversion < 0x02070000:
        return errfunc
    else:
        return func

class _IlocWrapper:
    def __init__(self, _list):
        self._list = _list
    def __len__(self):
        return len(self._list)
    def __getitem__(self, index):
        return self._list[index]

class SortedDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._dict = dict()
        self._list = SortedList()
        self.iloc = _IlocWrapper(self._list)

        if len(args) > 0:
            self.update(args[0])
        elif len(kwargs) > 0:
            self.update(**kwargs)

    def clear(self):
        self._dict.clear()
        self._list.clear()

    def __contains__(self, key):
        return key in self._dict

    def __delitem__(self, key):
        del self._dict[key]
        self._list.remove(key)

    def __getitem__(self, key):
        return self._dict[key]

    def __eq__(self, that):
        return (len(self) == len(that)
                and all(self[key] == that[key] for key in self))

    def __ne__(self, that):
        return (len(self) != len(that)
                or any(self[key] != that[key] for key in self))

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._dict)

    def __setitem__(self, key, value):
        if key not in self._dict:
            self._list.add(key)
        self._dict[key] = value

    def copy(self):
        that = SortedDict()
        that._dict = self._dict
        that._list = self._list
        that.iloc = self.iloc
        return that

    @classmethod
    def fromkeys(cls, seq, value=None):
        that = SortedDict()
        for key in seq:
            that[key] = value
        return that

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def has_key(self, key):
        return key in self._dict

    def items(self):
        if version_info[0] == 2:
            return list(self.iteritems())
        else:
            return ItemsView(self)

    def iteritems(self):
        for key in self._list:
            yield key, self._dict[key]

    def keys(self):
        if version_info[0] == 2:
            return SortedSet(self._dict)
        else:
            return KeysView(self)

    def iterkeys(self):
        return iter(self._list)

    def values(self):
        if version_info[0] == 2:
            return list(self.itervalues())
        else:
            return ValuesView(self)

    def itervalues(self):
        for key in self._list:
            yield self._dict[key]

    def pop(self, key, default=_NotGiven):
        if key in self._dict:
            self._list.remove(key)
            return self._dict.pop(key)
        else:
            if default == _NotGiven:
                raise KeyError
            else:
                return default

    def popitem(self):
        if len(self) == 0:
            raise KeyError
        key = self._list.pop()
        value = self._dict[key]
        del self._dict[key]
        return (key, value)

    def setdefault(self, key, default=None):
        if key in self._dict:
            return self._dict[key]
        else:
            self._dict[key] = default
            self._list.add(key)
            return default

    def update(self, other=None, **kwargs):
        if version_info[0] == 2:
            itr = kwargs.iteritems() if other is None else iter(other)
        else:
            itr = kwargs.items() if other is None else iter(other)

        for key, value in itr:
            self[key] = value

    def index(self, key, start=None, stop=None):
        """
        Return index of key in iteration.
        """
        return self._list.index(key, start, stop)

    @not26
    def viewkeys(self):
        return KeysView(self)

    @not26
    def viewvalues(self):
        return ValuesView(self)

    @not26
    def viewitems(self):
        return ItemsView(self)

    def _check(self):
        self._list._check()
        assert len(self._dict) == len(self._list)
        assert all(val in self._dict for val in self._list)

class KeysView:
    def __init__(self, sorted_dict):
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewkeys()
        else:
            self._view = sorted_dict._dict.keys()
    def __len__(self):
        return len(self._view)
    def __contains__(self, key):
        return key in self._view
    def __iter__(self):
        return iter(self._list)
    def __getitem__(self, index):
        return self._list[index]
    def __reversed__(self):
        return reversed(self._list)
    def index(self, value, start=None, stop=None):
        return self._list.index(value, start, stop)
    def count(self, value):
        return 1 if value in self._view else 0
    def __eq__(self, that):
        return self._view == that
    def __ne__(self, that):
        return self._view != that
    def __lt__(self, that):
        return self._view < that
    def __gt__(self, that):
        return self._view > that
    def __le__(self, that):
        return self._view <= that
    def __ge__(self, that):
        return self._view >= that
    def __and__(self, that):
        return SortedSet(self._view & that)
    def __or__(self, that):
        return SortedSet(self._view | that)
    def __sub__(self, that):
        return SortedSet(self._view - that)
    def __xor__(self, that):
        return SortedSet(self._view ^ that)
    def isdisjoint(self, that):
        return self._view.isdisjoint(that)
    def __repr__(self):
        return 'SortedDict_keys({0})'.format(repr(list(self)))

class ValuesView:
    def __init__(self, sorted_dict):
        self._dict = sorted_dict
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewvalues()
        else:
            self._view = sorted_dict._dict.values()
    def __len__(self):
        return len(self._dict)
    def __contains__(self, value):
        return value in self._view
    def __iter__(self):
        return iter(self._dict[key] for key in self._list)
    def __getitem__(self, index):
        if isinstance(idx, slice):
            return [self._dict[key] for key in self._list[index]]
        else:
            return self._dict[self._list[index]]
    def __reversed__(self):
        return iter(self._dict[key] for key in reversed(self._list))
    def index(self, key):
        for idx, value in enumerate(self):
            if key == value:
                return idx
        else:
            raise ValueError
    def count(self, key):
        return self._view.count(key)
    def __lt__(self, that):
        raise TypeError
    def __gt__(self, that):
        raise TypeError
    def __le__(self, that):
        raise TypeError
    def __ge__(self, that):
        raise TypeError
    def __and__(self, that):
        raise TypeError
    def __or__(self, that):
        raise TypeError
    def __sub__(self, that):
        raise TypeError
    def __xor__(self, that):
        raise TypeError
    def __repr__(self):
        return 'SortedDict_values({0})'.format(repr(list(self)))

class ItemsView:
    def __init__(self, sorted_dict):
        self._dict = sorted_dict
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewitems()
        else:
            self._view = sorted_dict._dict.items()
    def __len__(self):
        return len(self._view)
    def __contains__(self, key):
        return key in self._view
    def __iter__(self):
        return iter((key, self._dict[key]) for key in self._list)
    def __getitem__(self, index):
        if isinstance(idx, slice):
            return [(key, self._dict[key]) for key in self._list[index]]
        else:
            key = self._list[index]
            return (key, self._dict[key])
    def __reversed__(self):
        return iter((key, self._dict[key]) for key in reversed(self._list))
    def index(self, key, start=None, stop=None):
        pos = self._list.index(key[0], start, stop)
        if key[1] == self._dict[key[0]]:
            return pos
        else:
            raise ValueError
    def count(self, key):
        return self._view.count(key)
    def __eq__(self, that):
        return self._view == that
    def __ne__(self, that):
        return self._view != that
    def __lt__(self, that):
        return self._view < that
    def __gt__(self, that):
        return self._view > that
    def __le__(self, that):
        return self._view <= that
    def __ge__(self, that):
        return self._view >= that
    def __and__(self, that):
        return SortedSet(self._view & that)
    def __or__(self, that):
        return SortedSet(self._view | that)
    def __sub__(self, that):
        return SortedSet(self._view - that)
    def __xor__(self, that):
        return SortedSet(self._view ^ that)
    def isdisjoint(self, that):
        return self._view.isdisjoint(that)
    def __repr__(self):
        return 'SortedDict_items({0})'.format(repr(list(self)))
