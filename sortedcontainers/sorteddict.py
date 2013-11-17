"""
Sorted dict implementation.
"""

from sortedlist import SortedList
from collections import MutableMapping

_NotGiven = object()

class SortedDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._dict = dict()
        self._list = SortedList()

    def __contains__(self, key):
        return key in self._dict

    def __delitem__(self, key):
        del self._dict[key]
        self._list.remove(key)

    def __getitem__(self, key):
        return self._dict[key]

    def __eq__(self, that):
        raise NotImplementedError

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._dict)

    def __setitem__(self, key, value):
        if key not in self._dict:
            self._list.insert(key)
        self._dict[key] = value

    def copy(self):
        raise NotImplementedError

    def fromkeys(self, seq, value=None, key=None):
        raise NotImplementedError

    def get(self, key, default=None):
        if key in self._dict:
            return self._dict[key]
        else:
            return default

    def items(self):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def pop(self, key, default=_NotGiven):
        if key in self._dict:
            self._list.remove(key)
            return self._dict.pop[key]
        else:
            if default == SortedDict.__NotGiven:
                raise KeyError
            else:
                return default

    def popitem(self):
        key = self._list[0]
        value = self._dict[key]
        del self._list[0]
        del self._dict[key]
        return (key, value)

    def setdefault(self, default=None):
        if key in self._dict:
            return self._dict[key]
        else:
            self._dict[key] = default
            self._list.insert(key)
            return default

    def update(self, other=None, **kwargs):
        itr = iter(kwargs) if other is None else iter(other)

        for key, value in itr:
            self[key] = value

    def values(self):
        raise NotImplementedError

class KeyView:
    def __init__(self):
        raise NotImplementedError

class ValuesView:
    def __init__(self):
        raise NotImplementedError

class ItemsView:
    def __init__(self):
        raise NotImplementedError
