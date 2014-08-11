# -*- coding: utf-8 -*-
#
# Sorted set implementation.

from sys import version_info

from .sortedlist import SortedList, recursive_repr
from collections import MutableSet, Sequence
from itertools import chain

if version_info[0] == 2:
    from itertools import izip as zip

class SortedSet(MutableSet, Sequence):
    """
    A `SortedSet` provides the same methods as a `set`.  Additionally, a
    `SortedSet` maintains its items in sorted order, allowing the `SortedSet` to
    be indexed.

    Unlike a `set`, a `SortedSet` requires items be hashable and comparable.
    """
    def __init__(self, iterable=None, load=1000, _set=None):
        """
        A `SortedSet` provides the same methods as a `set`.  Additionally, a
        `SortedSet` maintains its items in sorted order, allowing the
        `SortedSet` to be indexed.

        An optional *iterable* provides an initial series of items to populate the
        `SortedSet`.

        An optional *load* specifies the load-factor of the set. The default
        load factor of '1000' works well for sets from tens to tens of millions
        of elements.  Good practice is to use a value that is the cube root of
        the set size.  With billions of elements, the best load factor depends
        on your usage.  It's best to leave the load factor at the default until
        you start benchmarking.
        """
        self._set = set() if _set is None else _set
        self._list = SortedList(self._set, load=load)
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
        if isinstance(index, slice):
            return SortedSet(self._list[index])
        else:
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
    def __setitem__(self, index, value):
        """
        Remove the element at position *index* and add *value* to the set.

        Supports slice notation and negative indexes.
        """
        _list, _set = self._list, self._set
        prev = _list[index]
        _list[index] = value

        if isinstance(index, slice):
            _set.difference_update(prev)
            _set.update(prev)
        else:
            _set.remove(prev)
            _set.add(prev)
    def __eq__(self, that):
        """Return True if and only if self and *that* are equal sets."""
        if len(self) != len(that):
            return False
        if isinstance(that, SortedSet):
            return (self._list == that._list)
        elif isinstance(that, set):
            return (self._set == that)
        else:
            _set = self._set
            return all(val in _set for val in that)
    def __ne__(self, that):
        """Return True if and only if self and *that* are inequal sets."""
        if len(self) != len(that):
            return True
        if isinstance(that, SortedSet):
            return (self._list != that._list)
        elif isinstance(that, set):
            return (self._set != that)
        else:
            _set = self._set
            return any(val not in _set for val in that)
    def __lt__(self, that):
        """Return True if and only if self is a subset of *that*."""
        if isinstance(that, set):
            return (self._set < that)
        else:
            return (len(self) < len(that)) and all(val in that for val in self._list)
    def __gt__(self, that):
        """Return True if and only if self is a superset of *that*."""
        if isinstance(that, set):
            return (self._set > that)
        else:
            _set = self._set
            return (len(self) > len(that)) and all(val in _set for val in that)
    def __le__(self, that):
        """Return True if and only if self is contained within *that*."""
        if isinstance(that, set):
            return (self._set <= that)
        else:
            return all(val in that for val in self._list)
    def __ge__(self, that):
        """Return True if and only if *that* is contained within self."""
        if isinstance(that, set):
            return (self._set >= that)
        else:
            _set = self._set
            return all(val in _set for val in that)
    def __and__(self, that):
        """
        Return a new SortedSet with the elements common to self and *that*.
        """
        return self.intersection(that)
    def __or__(self, that):
        """
        Return a new SortedSet containing all the elements in self and *that*.
        """
        return self.union(that)
    def __sub__(self, that):
        """
        Return a new SortedSet with elements in self that are not in *that*.
        """
        return self.difference(that)
    def __xor__(self, that):
        """
        Return a new SortedSet with elements in self or *that* but not both.
        """
        return self.symmetric_difference(that)
    def __iter__(self):
        """
        Return an iterator over the SortedSet. Elements are iterated over
        in their sorted order.
        """
        return iter(self._list)
    def __len__(self):
        """Return the number of elements in the set."""
        return len(self._set)
    def __reversed__(self):
        """Create an iterator to traverse the set in reverse."""
        return reversed(self._list)
    def add(self, value):
        """Add the element *value* to the set."""
        if value not in self._set:
            self._set.add(value)
            self._list.add(value)
    def bisect_left(self, value):
        """
        Similar to the ``bisect`` module in the standard library, this returns
        an appropriate index to insert *value* in SortedSet. If *value* is
        already present in SortedSet, the insertion point will be before (to the
        left of) any existing entries.
        """
        return self._list.bisect_left(value)
    def bisect(self, value):
        """Same as bisect_left."""
        return self._list.bisect(value)
    def bisect_right(self, value):
        """
        Same as `bisect_left`, but if *value* is already present in SortedSet,
        the insertion point will be after (to the right of) any existing
        entries.
        """
        return self._list.bisect_right(value)
    def clear(self):
        """Remove all elements from the set."""
        self._set.clear()
        self._list.clear()
    def copy(self):
        """Create a shallow copy of the sorted set."""
        return SortedSet(load=self._list._load, _set=set(self._set))
    def __copy__(self):
        """Create a shallow copy of the sorted set."""
        return self.copy()
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
    def index(self, value, start=None, stop=None):
        """
        Return the smallest *k* such that `SortedSet[k] == x` and `start <= k <
        stop`.  Raises ValueError if *value* is not present.  *stop* defaults to
        the end of the set.  *start* defaults to the beginning.  Negative
        indexes are supported, as for slice indices.
        """
        return self._list.index(value, start, stop)
    def isdisjoint(self, that):
        """
        Return True if the set has no elements in common with *that*.  Sets are
        disjoint if and only if their intersection is the empty set.
        """
        return self._set.isdisjoint(that)
    def issubset(self, that):
        """Test whether every element in the set is in *that*."""
        return self._set.issubset(that)
    def issuperset(self, that):
        """Test whether every element in *that* is in the set."""
        return self._set.issuperset(that)
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
        new_set = SortedSet(load=self._list._load, _set=diff)
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
        new_set = SortedSet(load=self._list._load, _set=comb)
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
        new_set = SortedSet(load=self._list._load, _set=diff)
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
        return SortedSet(chain(iter(self), *iterables), load=self._list._load)
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
