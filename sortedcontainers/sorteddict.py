# -*- coding: utf-8 -*-
#
# Sorted dict implementation.

from .sortedset import SortedSet
from .sortedlist import SortedList, recursive_repr
from collections import Mapping, MutableMapping, Set, Sequence
from collections import KeysView as AbstractKeysView
from collections import ValuesView as AbstractValuesView
from collections import ItemsView as AbstractItemsView

from functools import wraps
from sys import version_info, hexversion

_NotGiven = object()

def not26(func):
    """Function decorator for methods not implemented in Python 2.6."""

    @wraps(func)
    def errfunc(*args, **kwargs):
        raise NotImplementedError

    if hexversion < 0x02070000:
        return errfunc
    else:
        return func

class _IlocWrapper:
    def __init__(self, _dict):
        self._dict = _dict
    def __len__(self):
        return len(self._dict)
    def __getitem__(self, index):
        """
        Very efficiently return the key at index *index* in iteration. Supports
        negative indices and slice notation. Raises IndexError on invalid
        *index*.
        """
        return self._dict._list[index]
    def __delitem__(self, index):
        """
        Remove the ``sdict[sdict.iloc[index]]`` from *sdict*. Supports negative
        indices and slice notation. Raises IndexError on invalid *index*.
        """
        _temp = self._dict
        _list, _dict = _temp._list, _temp._dict

        if isinstance(index, slice):
            keys = _list[index]
            del _list[index]
            for key in keys:
                del _dict[key]
        else:
            key = _list[index]
            del _list[index]
            del _dict[key]

class SortedDict(MutableMapping):
    """
    A SortedDict provides the same methods as a dict.  Additionally, a
    SortedDict efficiently maintains its keys in sorted order. Consequently, the
    keys method will return the keys in sorted order, the popitem method will
    remove the item with the highest key, etc.
    """
    def __init__(self, *args, **kwargs):
        """
        A SortedDict provides the same methods as a dict.  Additionally, a
        SortedDict efficiently maintains its keys in sorted order. Consequently,
        the keys method will return the keys in sorted order, the popitem method
        will remove the item with the highest key, etc.

        An optional *load* argument defines the load factor of the internal list
        used to maintain sort order. If present, this argument must come first
        and must be an integer. The default load factor of '1000' works well for
        lists from tens to tens of millions of elements.  Good practice is to
        use a value that is the cube root of the list size.  With billions of
        elements, the best load factor depends on your usage.  It's best to
        leave the load factor at the default until you start benchmarking.

        An optional *iterable* argument provides an initial series of items to
        populate the SortedDict.  Each item in the series must itself contain
        two items.  The first is used as a key in the new dictionary, and the
        second as the key's value. If a given key is seen more than once, the
        last value associated with it is retained in the new dictionary.

        If keyword arguments are given, the keywords themselves with their
        associated values are added as items to the dictionary. If a key is
        specified both in the positional argument and as a keyword argument, the
        value associated with the keyword is retained in the dictionary. For
        example, these all return a dictionary equal to ``{"one": 2, "two":
        3}``:

        * ``SortedDict(one=2, two=3)``
        * ``SortedDict({'one': 2, 'two': 3})``
        * ``SortedDict(zip(('one', 'two'), (2, 3)))``
        * ``SortedDict([['two', 3], ['one', 2]])``

        The first example only works for keys that are valid Python
        identifiers; the others work with any valid keys.
        """
        if len(args) > 0 and type(args[0]) == int:
            load = args[0]
            args = args[1:]
        else:
            load = 1000

        self._dict = dict()
        self._list = SortedList(load=load)
        self.iloc = _IlocWrapper(self)

        self.update(*args, **kwargs)

    def clear(self):
        """Remove all elements from the dictionary."""
        self._dict.clear()
        self._list.clear()

    def __contains__(self, key):
        """Return True if and only if *key* is in the dictionary."""
        return key in self._dict

    def __delitem__(self, key):
        """
        Remove ``d[key]`` from *d*.  Raises a KeyError if *key* is not in the
        dictionary.
        """
        del self._dict[key]
        self._list.remove(key)

    def __getitem__(self, key):
        """
        Return the item of *d* with key *key*.  Raises a KeyError if *key* is
        not in the dictionary.
        """
        return self._dict[key]

    def __eq__(self, that):
        """Compare two iterables for equality."""
        return (len(self._dict) == len(that)
                and all((key in that) and (self[key] == that[key])
                        for key in self))

    def __ne__(self, that):
        """Compare two iterables for inequality."""
        return (len(self._dict) != len(that)
                or any((key not in that) or (self[key] != that[key])
                       for key in self))

    def __iter__(self):
        """Create an iterator over the sorted keys of the dictionary."""
        return iter(self._list)

    def __reversed__(self):
        """
        Create a reversed iterator over the sorted keys of the dictionary.
        """
        return reversed(self._list)

    def __len__(self):
        """Return the number of (key, value) pairs in the dictionary."""
        return len(self._dict)

    def __setitem__(self, key, value):
        """Set `d[key]` to *value*."""
        _dict = self._dict
        if key not in _dict:
            self._list.add(key)
        _dict[key] = value

    def copy(self):
        """Return a shallow copy of the sorted dictionary."""
        return SortedDict(self._list._load, self._dict)

    def __copy__(self):
        """Return a shallow copy of the sorted dictionary."""
        return self.copy()

    @classmethod
    def fromkeys(cls, seq, value=None):
        """
        Create a new dictionary with keys from *seq* and values set to *value*.
        """
        that = SortedDict((key, value) for key in seq)
        return that

    def get(self, key, default=None):
        """
        Return the value for *key* if *key* is in the dictionary, else
        *default*.  If *default* is not given, it defaults to ``None``,
        so that this method never raises a KeyError.
        """
        return self._dict.get(key, default)

    def has_key(self, key):
        """Return True if and only in *key* is in the dictionary."""
        return key in self._dict

    def items(self):
        """
        In Python 2, returns a list of the dictionary's items (``(key, value)``
        pairs).

        In Python 3, returns a new ItemsView of the dictionary's items.  In
        addition to the methods provided by the built-in `view` the ItemsView is
        indexable (e.g., ``d.items()[5]``).
        """
        if version_info[0] == 2:
            return list(self.iteritems())
        else:
            return ItemsView(self)

    def iteritems(self):
        """Return an iterable over the items (``(key, value)`` pairs)."""
        _dict = self._dict
        return iter((key, _dict[key]) for key in self._list)

    def keys(self):
        """
        In Python 2, return a SortedSet of the dictionary's keys.

        In Python 3, return a new KeysView of the dictionary's keys.  In
        addition to the methods provided by the built-in `view` the KeysView is
        indexable (e.g., ``d.keys()[5]``).
        """
        if version_info[0] == 2:
            return SortedSet(self._dict)
        else:
            return KeysView(self)

    def iterkeys(self):
        """Return an iterable over the keys of the dictionary."""
        return iter(self._list)

    def values(self):
        """
        In Python 2, return a list of the dictionary's values.

        In Python 3, return a new :class:`ValuesView` of the dictionary's
        values.  In addition to the methods provided by the built-in `view`
        the ValuesView is indexable (e.g., ``d.values()[5]``).
        """
        if version_info[0] == 2:
            return list(self.itervalues())
        else:
            return ValuesView(self)

    def itervalues(self):
        """Return an iterable over the values of the dictionary."""
        _dict = self._dict
        return iter(_dict[key] for key in self._list)

    def pop(self, key, default=_NotGiven):
        """
        If *key* is in the dictionary, remove it and return its value,
        else return *default*. If *default* is not given and *key* is not in
        the dictionary, a KeyError is raised.
        """
        if key in self._dict:
            self._list.remove(key)
            return self._dict.pop(key)
        else:
            if default == _NotGiven:
                raise KeyError
            else:
                return default

    def popitem(self):
        """
        Remove and return the ``(key, value)`` pair with the greatest *key*
        from the dictionary.

        If the dictionary is empty, calling `popitem` raises a
        KeyError`.
        """
        _dict, _list = self._dict, self._list

        if len(_dict) == 0:
            raise KeyError

        key = _list.pop()
        value = _dict[key]
        del _dict[key]

        return (key, value)

    def setdefault(self, key, default=None):
        """
        If *key* is in the dictionary, return its value.  If not, insert *key*
        with a value of *default* and return *default*.  *default* defaults to
        ``None``.
        """
        _dict = self._dict
        if key in _dict:
            return _dict[key]
        else:
            _dict[key] = default
            self._list.add(key)
            return default

    def update(self, *args, **kwargs):
        """
        Update the dictionary with the key/value pairs from *other*, overwriting
        existing keys.

        *update* accepts either another dictionary object or an iterable of
        key/value pairs (as a tuple or other iterable of length two).  If
        keyword arguments are specified, the dictionary is then updated with
        those key/value pairs: ``d.update(red=1, blue=2)``.
        """
        _dict, _list = self._dict, self._list

        if len(_dict) == 0:
            _dict.update(*args, **kwargs)
            _list.update(_dict)
            return

        if (len(kwargs) == 0 and len(args) == 1 and isinstance(args[0], dict)):
            pairs = args[0]
        else:
            pairs = dict(*args, **kwargs)

        if (10 * len(pairs)) > len(self._dict):
            self._dict.update(pairs)
            _list = self._list
            _list.clear()
            _list.update(self._dict)
        else:
            for key in pairs:
                self[key] = pairs[key]

    def index(self, key, start=None, stop=None):
        """
        Return the smallest *k* such that `d.iloc[k] == key` and `i <= k < j`.
        Raises `ValueError` if *key* is not present.  *stop* defaults to the end
        of the set.  *start* defaults to the beginning.  Negative indexes are
        supported, as for slice indices.
        """
        return self._list.index(key, start, stop)

    def bisect_left(self, key):
        """
        Similar to the ``bisect`` module in the standard library, this returns
        an appropriate index to insert *key* in SortedDict. If *key* is
        already present in SortedDict, the insertion point will be before (to the
        left of) any existing entries.
        """
        return self._list.bisect_left(key)

    def bisect(self, key):
        """Same as bisect_left."""
        return self._list.bisect(key)

    def bisect_right(self, key):
        """
        Same as `bisect_left`, but if *key* is already present in SortedDict,
        the insertion point will be after (to the right of) any existing
        entries.
        """
        return self._list.bisect_right(key)

    @not26
    def viewkeys(self):
        """
        In Python 2.7 and later, return a new `KeysView` of the dictionary's
        keys.

        In Python 2.6, raise a NotImplementedError.
        """
        return KeysView(self)

    @not26
    def viewvalues(self):
        """
        In Python 2.7 and later, return a new `ValuesView` of the dictionary's
        values.

        In Python 2.6, raise a NotImplementedError.
        """
        return ValuesView(self)

    @not26
    def viewitems(self):
        """
        In Python 2.7 and later, return a new `ItemsView` of the dictionary's
        items.

        In Python 2.6, raise a NotImplementedError.
        """
        return ItemsView(self)

    @recursive_repr
    def __repr__(self):
        _dict = self._dict
        items = ', '.join('{0}: {1}'.format(repr(key), repr(_dict[key]))
                          for key in self._list)
        return '{0}({{{1}}})'.format(self.__class__.__name__, items)

    def _check(self):
        self._list._check()
        assert len(self._dict) == len(self._list)
        assert all(val in self._dict for val in self._list)

class KeysView(AbstractKeysView, Set, Sequence):
    """
    A KeysView object is a dynamic view of the dictionary's keys, which
    means that when the dictionary's keys change, the view reflects
    those changes.

    The KeysView class implements the Set and Sequence Abstract Base Classes.
    """
    def __init__(self, sorted_dict):
        """
        Initialize a KeysView from a SortedDict container as *sorted_dict*.
        """
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewkeys()
        else:
            self._view = sorted_dict._dict.keys()
    def __len__(self):
        """Return the number of entries in the dictionary."""
        return len(self._view)
    def __contains__(self, key):
        """
        Return True if and only if *key* is one of the underlying dictionary's
        keys.
        """
        return key in self._view
    def __iter__(self):
        """
        Return an iterable over the keys in the dictionary. Keys are iterated
        over in their sorted order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        return iter(self._list)
    def __getitem__(self, index):
        """Return the key at position *index*."""
        return self._list[index]
    def __reversed__(self):
        """
        Return a reversed iterable over the keys in the dictionary. Keys are
        iterated over in their reverse sort order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        return reversed(self._list)
    def index(self, value, start=None, stop=None):
        """
        Return the smallest *k* such that `keysview[k] == value` and `start <= k
        < end`.  Raises `KeyError` if *value* is not present.  *stop* defaults
        to the end of the set.  *start* defaults to the beginning.  Negative
        indexes are supported, as for slice indices.
        """
        return self._list.index(value, start, stop)
    def count(self, value):
        """Return the number of occurrences of *value* in the set."""
        return 1 if value in self._view else 0
    def __eq__(self, that):
        """Test set-like equality with *that*."""
        return self._view == that
    def __ne__(self, that):
        """Test set-like inequality with *that*."""
        return self._view != that
    def __lt__(self, that):
        """Test whether self is a proper subset of *that*."""
        return self._view < that
    def __gt__(self, that):
        """Test whether self is a proper superset of *that*."""
        return self._view > that
    def __le__(self, that):
        """Test whether self is contained within *that*."""
        return self._view <= that
    def __ge__(self, that):
        """Test whether *that* is contained within self."""
        return self._view >= that
    def __and__(self, that):
        """Return a SortedSet of the intersection of self and *that*."""
        return SortedSet(self._view & that)
    def __or__(self, that):
        """Return a SortedSet of the union of self and *that*."""
        return SortedSet(self._view | that)
    def __sub__(self, that):
        """Return a SortedSet of the difference of self and *that*."""
        return SortedSet(self._view - that)
    def __xor__(self, that):
        """Return a SortedSet of the symmetric difference of self and *that*."""
        return SortedSet(self._view ^ that)
    def isdisjoint(self, that):
        """Return True if and only if *that* is disjoint with self."""
        if version_info[0] == 2:
            return not any(key in self._list for key in that)
        else:
            return self._view.isdisjoint(that)
    @recursive_repr
    def __repr__(self):
        return 'SortedDict_keys({0})'.format(repr(list(self)))

class ValuesView(AbstractValuesView, Sequence):
    """
    A ValuesView object is a dynamic view of the dictionary's values, which
    means that when the dictionary's values change, the view reflects those
    changes.

    The ValuesView class implements the Sequence Abstract Base Class.
    """
    def __init__(self, sorted_dict):
        """
        Initialize a ValuesView from a SortedDict container as *sorted_dict*.
        """
        self._dict = sorted_dict
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewvalues()
        else:
            self._view = sorted_dict._dict.values()
    def __len__(self):
        """Return the number of entries in the dictionary."""
        return len(self._dict)
    def __contains__(self, value):
        """
        Return True if and only if *value* is on the underlying dictionary's
        values.
        """
        return value in self._view
    def __iter__(self):
        """
        Return an iterator over the values in the dictionary.  Values are
        iterated over in sorted order of the keys.

        Iterating views while adding or deleting entries in the dictionary may
        raise a `RuntimeError` or fail to iterate over all entries.
        """
        _dict = self._dict
        return iter(_dict[key] for key in self._list)
    def __getitem__(self, index):
        """
        Efficiently return value at *index* in iteration.

        Supports slice notation and negative indexes.
        """
        _dict, _list = self._dict, self._list
        if isinstance(index, slice):
            return [_dict[key] for key in _list[index]]
        else:
            return _dict[_list[index]]
    def __reversed__(self):
        """
        Return a reverse iterator over the values in the dictionary.  Values are
        iterated over in reverse sort order of the keys.

        Iterating views while adding or deleting entries in the dictionary may
        raise a `RuntimeError` or fail to iterate over all entries.
        """
        _dict = self._dict
        return iter(_dict[key] for key in reversed(self._list))
    def index(self, value):
        """
        Return index of *value* in self.

        Raises ValueError if *value* is not found.
        """
        for idx, val in enumerate(self):
            if value == val:
                return idx
        else:
            raise ValueError
    def count(self, value):
        """Return the number of occurrences of *value* in self."""
        _dict = self._dict
        if version_info[0] == 2:
            return sum(1 for val in _dict.itervalues() if val == value)
        else:
            return sum(1 for val in _dict.values() if val == value)
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
    @recursive_repr
    def __repr__(self):
        return 'SortedDict_values({0})'.format(repr(list(self)))

class ItemsView(AbstractItemsView, Set, Sequence):
    """
    An ItemsView object is a dynamic view of the dictionary's ``(key,
    value)`` pairs, which means that when the dictionary changes, the
    view reflects those changes.

    The ItemsView class implements the Set and Sequence Abstract Base Classes.
    However, the set-like operations (``&``, ``|``, ``-``, ``^``) will only
    operate correctly if all of the dictionary's values are hashable.
    """
    def __init__(self, sorted_dict):
        """
        Initialize an ItemsView from a SortedDict container as *sorted_dict*.
        """
        self._dict = sorted_dict
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewitems()
        else:
            self._view = sorted_dict._dict.items()
    def __len__(self):
        """Return the number of entries in the dictionary."""
        return len(self._view)
    def __contains__(self, key):
        """
        Return True if and only if *key* is one of the underlying dictionary's
        items.
        """
        return key in self._view
    def __iter__(self):
        """
        Return an iterable over the items in the dictionary. Items are iterated
        over in their sorted order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        _dict = self._dict
        return iter((key, _dict[key]) for key in self._list)
    def __getitem__(self, index):
        """Return the item as position *index*."""
        _dict, _list = self._dict, self._list
        if isinstance(index, slice):
            return [(key, _dict[key]) for key in _list[index]]
        else:
            key = _list[index]
            return (key, _dict[key])
    def __reversed__(self):
        """
        Return a reversed iterable over the items in the dictionary. Items are
        iterated over in their reverse sort order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        _dict = self._dict
        return iter((key, _dict[key]) for key in reversed(self._list))
    def index(self, key, start=None, stop=None):
        """
        Return the smallest *k* such that `itemssview[k] == key` and `start <= k
        < end`.  Raises `KeyError` if *key* is not present.  *stop* defaults
        to the end of the set.  *start* defaults to the beginning.  Negative
        indexes are supported, as for slice indices.
        """
        pos = self._list.index(key[0], start, stop)
        if key[1] == self._dict[key[0]]:
            return pos
        else:
            raise ValueError
    def count(self, item):
        """Return the number of occurrences of *item* in the set."""
        key, value = item
        return 1 if key in self._dict and self._dict[key] == value else 0
    def __eq__(self, that):
        """Test set-like equality with *that*."""
        return self._view == that
    def __ne__(self, that):
        """Test set-like inequality with *that*."""
        return self._view != that
    def __lt__(self, that):
        """Test whether self is a proper subset of *that*."""
        return self._view < that
    def __gt__(self, that):
        """Test whether self is a proper superset of *that*."""
        return self._view > that
    def __le__(self, that):
        """Test whether self is contained within *that*."""
        return self._view <= that
    def __ge__(self, that):
        """Test whether *that* is contained within self."""
        return self._view >= that
    def __and__(self, that):
        """Return a SortedSet of the intersection of self and *that*."""
        return SortedSet(self._view & that)
    def __or__(self, that):
        """Return a SortedSet of the union of self and *that*."""
        return SortedSet(self._view | that)
    def __sub__(self, that):
        """Return a SortedSet of the difference of self and *that*."""
        return SortedSet(self._view - that)
    def __xor__(self, that):
        """Return a SortedSet of the symmetric difference of self and *that*."""
        return SortedSet(self._view ^ that)
    def isdisjoint(self, that):
        """Return True if and only if *that* is disjoint with self."""
        if version_info[0] == 2:
            _dict = self._dict
            for key, value in that:
                if key in _dict and _dict[key] == value:
                    return False
            return True
        else:
            return self._view.isdisjoint(that)
    @recursive_repr
    def __repr__(self):
        return 'SortedDict_items({0})'.format(repr(list(self)))
