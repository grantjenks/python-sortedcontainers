# -*- coding: utf-8 -*-
#
# Sorted set implementation.

from .sortedlist import SortedList, recursive_repr
from .sortedlistwithkey import SortedListWithKey
from collections import Set, MutableSet, Sequence
from itertools import chain

class SortedSet(MutableSet, Sequence):
    """
    A `SortedSet` provides the same methods as a `set`.  Additionally, a
    `SortedSet` maintains its items in sorted order, allowing the `SortedSet` to
    be indexed.

    Unlike a `set`, a `SortedSet` requires items be hashable and comparable.
    """
    def __init__(self, iterable=None, key=None, load=1000, _set=None):
        """
        A `SortedSet` provides the same methods as a `set`.  Additionally, a
        `SortedSet` maintains its items in sorted order, allowing the
        `SortedSet` to be indexed.

        An optional *iterable* provides an initial series of items to populate
        the `SortedSet`.

        An optional *key* argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each set item. If no function is specified, the default compares the
        set items directly.

        An optional *load* specifies the load-factor of the set. The default
        load factor of '1000' works well for sets from tens to tens of millions
        of elements.  Good practice is to use a value that is the cube root of
        the set size.  With billions of elements, the best load factor depends
        on your usage.  It's best to leave the load factor at the default until
        you start benchmarking.
        """
        self._key = key
        self._load = load

        self._set = set() if _set is None else _set

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        if key is None:
            self._list = SortedList(self._set, load=load)
        else:
            self._list = SortedListWithKey(self._set, key=key, load=load)

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index

        if iterable is not None:
            self.update(iterable)

    def __contains__(self, value):
        """Return True if and only if *value* is an element in the set."""
        return (value in self._set)

    def __getitem__(self, index):
        """
        Return the element at position *index*.

        Supports slice notation and negative indexes.
        """
        return self._list[index]

    def __delitem__(self, index):
        """
        Remove the element at position *index*.

        Supports slice notation and negative indexes.
        """
        _list = self._list
        if isinstance(index, slice):
            values = _list[index]
            self._set.difference_update(values)
        else:
            value = _list[index]
            self._set.remove(value)
        del _list[index]

    def __eq__(self, that):
        """Return True if and only if self and *that* are equal sets."""
        if len(self) != len(that):
            return False
        elif isinstance(that, SortedSet):
            return (self._set == that._set)
        elif isinstance(that, Set):
            return (self._set == that)
        else:
            raise TypeError('can only compare to a Set')

    def __ne__(self, that):
        """Return True if and only if self and *that* are inequal sets."""
        if len(self) != len(that):
            return True
        elif isinstance(that, SortedSet):
            return (self._set != that._set)
        elif isinstance(that, Set):
            return (self._set != that)
        else:
            raise TypeError('can only compare to a Set')

    def __lt__(self, that):
        """Return True if and only if self is a subset of *that*."""
        if len(self) >= len(that):
            return False
        elif isinstance(that, SortedSet):
            return (self._set < that._set)
        elif isinstance(that, Set):
            return (self._set < that)
        else:
            raise TypeError('can only compare to a Set')

    def __gt__(self, that):
        """Return True if and only if self is a superset of *that*."""
        if len(self) <= len(that):
            return False
        elif isinstance(that, SortedSet):
            return (self._set > that._set)
        elif isinstance(that, Set):
            return (self._set > that)
        else:
            raise TypeError('can only compare to a Set')

    def __le__(self, that):
        """Return True if and only if self is contained within *that*."""
        if len(self) > len(that):
            return False
        elif isinstance(that, SortedSet):
            return (self._set <= that._set)
        elif isinstance(that, Set):
            return (self._set <= that)
        else:
            raise TypeError('can only compare to a Set')

    def __ge__(self, that):
        """Return True if and only if *that* is contained within self."""
        if len(self) < len(that):
            return False
        elif isinstance(that, SortedSet):
            return (self._set >= that._set)
        elif isinstance(that, Set):
            return (self._set >= that)
        else:
            raise TypeError('can only compare to a Set')

    def __and__(self, that):
        """
        Return a new SortedSet with the elements common to self and *that*.
        """
        return self.intersection(that)

    __rand__ = __and__

    def __iand__(self, that):
        """
        Update the set, keeping only elements found in self and *that*.
        """
        self.intersection_update(that)
        return self

    def __or__(self, that):
        """
        Return a new SortedSet containing all the elements in self or *that*.
        """
        return self.union(that)

    __ror__ = __or__

    def __ior__(self, that):
        """
        Update the set, adding elements found in *that*.
        """
        self.update(that)
        return self

    def __sub__(self, that):
        """
        Return a new SortedSet with elements in self that are not in *that*.
        """
        return self.difference(that)

    __rsub__ = __sub__

    def __isub__(self, that):
        """
        Update the set, removing elements found in *that*.
        """
        self.difference_update(that)
        return self

    def __xor__(self, that):
        """
        Return a new SortedSet with elements in self or *that* but not both.
        """
        return self.symmetric_difference(that)

    __rxor__ = __xor__

    def __ixor__(self, that):
        """
        Update the set, include only elements in self or *that* but not both.
        """
        self.symmetric_difference_update(that)
        return self

    def __len__(self):
        """Return the number of elements in the set."""

        return len(self._set)

    def __iter__(self):
        """
        Return an iterator over the SortedSet. Elements are iterated over
        in their sorted order.
        """
        return iter(self._list)

    def __reversed__(self):
        """
        Return an iterator over the SortedSet. Elements are iterated over
        in their reversed sorted order.
        """
        return reversed(self._list)

    def add(self, value):
        """Add the element *value* to the set."""
        if value not in self._set:
            self._set.add(value)
            self._list.add(value)

    def clear(self):
        """Remove all elements from the set."""
        self._set.clear()
        self._list.clear()

    def copy(self):
        """Create a shallow copy of the sorted set."""
        return SortedSet(key=self._key, load=self._load, _set=set(self._set))

    __copy__ = copy

    def count(self, value):
        """Return the number of occurrences of *value* in the set."""
        return 1 if value in self._set else 0

    def discard(self, value):
        """
        Remove the first occurrence of *value*.  If *value* is not a member,
        does nothing.
        """
        if value in self._set:
            self._set.remove(value)
            self._list.discard(value)

    def pop(self, index=-1):
        """
        Remove and return item at *index* (default last).  Raises IndexError if
        set is empty or index is out of range.  Negative indexes are supported,
        as for slice indices.
        """
        value = self._list.pop(index)
        self._set.remove(value)
        return value

    def remove(self, value):
        """
        Remove first occurrence of *value*.  Raises ValueError if
        *value* is not present.
        """
        self._set.remove(value)
        self._list.remove(value)

    def difference(self, *iterables):
        """
        Return a new set with elements in the set that are not in the
        *iterables*.
        """
        diff = self._set.difference(*iterables)
        new_set = SortedSet(key=self._key, load=self._load, _set=diff)
        return new_set

    def difference_update(self, *iterables):
        """
        Update the set, removing elements found in keeping only elements
        found in any of the *iterables*.
        """
        values = set(chain(*iterables))
        if (4 * len(values)) > len(self):
            self._set.difference_update(values)
            self._list.clear()
            self._list.update(self._set)
        else:
            _discard = self.discard
            for value in values:
                _discard(value)

    def intersection(self, *iterables):
        """
        Return a new set with elements common to the set and all *iterables*.
        """
        comb = self._set.intersection(*iterables)
        new_set = SortedSet(key=self._key, load=self._load, _set=comb)
        return new_set

    def intersection_update(self, *iterables):
        """
        Update the set, keeping only elements found in it and all *iterables*.
        """
        self._set.intersection_update(*iterables)
        self._list.clear()
        self._list.update(self._set)

    def symmetric_difference(self, that):
        """
        Return a new set with elements in either *self* or *that* but not both.
        """
        diff = self._set.symmetric_difference(that)
        new_set = SortedSet(key=self._key, load=self._load, _set=diff)
        return new_set

    def symmetric_difference_update(self, that):
        """
        Update the set, keeping only elements found in either *self* or *that*,
        but not in both.
        """
        self._set.symmetric_difference_update(that)
        self._list.clear()
        self._list.update(self._set)

    def union(self, *iterables):
        """
        Return a new SortedSet with elements from the set and all *iterables*.
        """
        return SortedSet(chain(iter(self), *iterables), key=self._key, load=self._load)

    def update(self, *iterables):
        """Update the set, adding elements from all *iterables*."""
        values = set(chain(*iterables))
        if (4 * len(values)) > len(self):
            self._set.update(values)
            self._list.clear()
            self._list.update(self._set)
        else:
            _add = self.add
            for value in values:
                _add(value)

    @recursive_repr
    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, repr(list(self)))

    def _check(self):
        self._list._check()
        assert len(self._set) == len(self._list)
        _set = self._set
        assert all(val in _set for val in self._list)
