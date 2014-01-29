"""
Sorted dict implementation.
"""

from .sortedset import SortedSet
from .sortedlist import SortedList
from collections import MutableMapping

from sys import version_info

_NotGiven = object()

def not26(func):
    from functools import wraps

    @wraps(func)
    def errfunc(*args, **kwargs):
        raise NotImplementedError

    if version_info[0] == 2:
        return errfunc
    else:
        return func

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
        return all(self[key] == that[key] for key in that)

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
            return self.iteritems()
        else:
            return list(self.iteritems())

    def iteritems(self):
        for key in self._list:
            yield key, self._dict[key]

    def keys(self):
        if version_info[0] == 2:
            return self.iterkeys()
        else:
            return list(self.iterkeys())

    def iterkeys(self):
        return iter(self._list)

    def values(self):
        if version_info[0] == 2:
            return self.itervalues()
        else:
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

    def iloc(self, index):
        """
        Return key(s) corresponding to index location.
        Accepts slices.
        Use to easily implement find_min or pop_max. For example:

            def find_min(sdict):
                return sdict.iloc(0)

            def pop_max(sdict):
                val = sdict.iloc(-1)
                del sdict[val]
                return val
        """
        return self._list[index]

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
        self._view = sorted_dict._dict.viewkeys()
    def __len__(self):
        return len(self._view)
    def __contains__(self, key):
        return key in self._view
    def __iter__(self):
        return iter(self._list)
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
    def __repr__(self):
        return 'SortedDict_keys({0})'.format(repr(list(self)))

class ValuesView:
    def __init__(self, sorted_dict):
        self._dict = sorted_dict
        self._list = sorted_dict._list
        self._view = sorted_dict._dict.viewvalues()
    def __len__(self):
        return len(self._dict)
    def __contains__(self, key):
        return key in self._view
    def __iter__(self):
        return iter(self._dict[key] for key in self._list)
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
        self._view = sorted_dict._dict.viewitems()
    def __len__(self):
        return len(self._view)
    def __contains__(self, key):
        return key in self._view
    def __iter__(self):
        return iter((key, self._dict[key]) for key in self._list)
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
    def __repr__(self):
        return 'SortedDict_items({0})'.format(repr(list(self)))
