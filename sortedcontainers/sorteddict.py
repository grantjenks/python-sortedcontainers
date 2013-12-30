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
        that = SortedDict()
        that._dict = self._dict
        that._list = self._list
        return that

    @classmethod
    def fromkeys(self, seq, value=None):
        that = SortedDict()
        for key in seq:
            that[key] = value
        return that

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def has_key(self, key):
        return self._dict.has_key(key)

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        for key in self._list:
            yield key, self._dict[key]

    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        return iter(self._list)

    def values(self):
        return list(self.itervalues())

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
        key = self._list.pop()
        value = self._dict[key]
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

    def viewkeys(self):
        return KeysView(self)

    def viewvalues(self):
        return ValuesView(self)

    def viewitems(self):
        return ItemsView(self)

class KeysView:
    def __init__(self, sdict):
        self._sdict = sdict
    def __len__(self):
        return len(self._sdict)
    def __contains__(self, key):
        return key in self._sdict
    def __and__(self, that):
        raise NotImplementedError
    def __or__(self, that):
        raise NotImplementedError
    def __sub__(self, that):
        raise NotImplementedError
    def __xor__(self, that):
        raise NotImplementedError

class ValuesView:
    def __init__(self, sdict):
        self._sdict = sdict
    def __len__(self):
        return len(self._sdict)
    def __contains__(self, value):
        return any(value == other for other in self._sdict.itervalues())
    def __and__(self, that):
        raise NotImplementedError
    def __or__(self, that):
        raise NotImplementedError
    def __sub__(self, that):
        raise NotImplementedError
    def __xor__(self, that):
        raise NotImplementedError

class ItemsView:
    def __init__(self, sdict):
        self._sdict = sdict
    def __len__(self):
        return len(self._sdict)
    def __contains__(self, item):
        key, value = item
        return key in self._sdict and self._sdict[key] == value
    def __and__(self, that):
        raise NotImplementedError
    def __or__(self, that):
        raise NotImplementedError
    def __sub__(self, that):
        raise NotImplementedError
    def __xor__(self, that):
        raise NotImplementedError
