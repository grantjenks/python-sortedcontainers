# -*- coding: utf-8 -*-
#
# Sorted list with key implementation.

from sys import hexversion
from .sortedlist import SortedList, recursive_repr
from collections import MutableSequence
from bisect import bisect_left

if hexversion < 0x03000000:
    range = xrange

class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __eq__(self, that):
        return self.key == that.key
    def __ne__(self, that):
        return self.key != that.key
    def __lt__(self, that):
        return self.key < that.key
    def __le__(self, that):
        return self.key <= that.key
    def __gt__(self, that):
        return self.key > that.key
    def __ge__(self, that):
        return self.key >= that.key
    @recursive_repr
    def __repr__(self):
        return 'Pair({0}, {1})'.format(repr(self.key), repr(self.value))

def identity(value):
    return value

class SortedListWithKey(MutableSequence):
    """
    SortedListWithKey provides most of the same methods as a list but keeps the
    items in sorted order.
    """

    def __init__(self, iterable=None, key=identity, load=1000):
        """
        A SortedListWithKey provides most of the same methods as a list, but
        keeps the items in sorted order.

        An optional *iterable* provides an initial series of items to
        populate the SortedListWithKey.

        An optional *load* specifies the load-factor of the list. The default
        load factor of '1000' works well for lists from tens to tens of millions
        of elements.  Good practice is to use a value that is the square or cube
        root of the list size.  With billions of elements, the best load factor
        depends on your usage.  It's best to leave the load factor at the
        default until you start benchmarking. See implementation details for
        more information.

        An optional *key* argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each element. The default is the identity function.

        An optional *key* specifies a key function to apply to inserted
        values. Values will be ordered by their key. A SortedListWithKey
        must maintain the sort order at all times.

        SortedListWithKey implements the MutableSequence Abstract Base Class
        type.
        """
        self._key = key
        self._load = load
        self._list = SortedList(load=load)

        if iterable is not None:
            self.update(iterable)

    def clear(self):
        """Remove all the elements from the list."""
        self._list.clear()

    def add(self, value):
        """Add the element *value* to the list."""
        self._list.add(Pair(self._key(value), value))

    def update(self, iterable):
        """Update the list by adding all elements from *iterable*."""
        _key = self._key
        self._list.update(Pair(_key(val), val) for val in iterable)

    def __contains__(self, value):
        """Return True if and only if *value* is an element in the list."""
        _list = self._list
        _key = self._key(value)
        _pair = Pair(_key, value)

        _maxes = _list._maxes

        if not _maxes:
            return False

        pos = bisect_left(_maxes, _pair)

        if pos == len(_maxes):
            return False

        _lists = _list._lists

        idx = bisect_left(_lists[pos], _pair)

        len_lists = len(_lists)
        len_sublist = len(_lists[pos])

        while True:
            pair = _lists[pos][idx]
            if _key != pair.key:
                return False
            if value == pair.value:
                return True
            idx += 1
            if idx == len_sublist:
                pos += 1
                if pos == len_lists:
                    return False
                len_sublist = len(_lists[pos])
                idx = 0

    def discard(self, value):
        """
        Remove the first occurrence of *value*.

        If *value* is not a member, does nothing.
        """
        _list = self._list
        _key = self._key(value)
        _pair = Pair(_key, value)

        _maxes = _list._maxes

        if not _maxes:
            return

        pos = bisect_left(_maxes, _pair)

        if pos == len(_maxes):
            return

        _lists = _list._lists

        idx = bisect_left(_lists[pos], _pair)

        len_lists = len(_lists)
        len_sublist = len(_lists[pos])

        while True:
            pair = _lists[pos][idx]
            if _key != pair.key:
                return
            if value == pair.value:
                _list._delete(pos, idx)
                return
            idx += 1
            if idx == len_sublist:
                pos += 1
                if pos == len_lists:
                    return
                len_sublist = len(_lists[pos])
                idx = 0

    def remove(self, value):
        """
        Remove first occurrence of *value*.

        Raises ValueError if *value* is not present.
        """
        _list = self._list
        _key = self._key(value)
        _pair = Pair(_key, value)

        _maxes = _list._maxes

        if not _maxes:
            raise ValueError('{0} is not in list'.format(repr(value)))

        pos = bisect_left(_maxes, _pair)

        if pos == len(_maxes):
            raise ValueError('{0} is not in list'.format(repr(value)))

        _lists = _list._lists

        idx = bisect_left(_lists[pos], _pair)

        len_lists = len(_lists)
        len_sublist = len(_lists[pos])

        while True:
            pair = _lists[pos][idx]
            if _key != pair.key:
                raise ValueError('{0} is not in list'.format(repr(value)))
            if value == pair.value:
                _list._delete(pos, idx)
                return
            idx += 1
            if idx == len_sublist:
                pos += 1
                if pos == len_lists:
                    raise ValueError('{0} is not in list'.format(repr(value)))
                len_sublist = len(_lists[pos])
                idx = 0

    def __delitem__(self, index):
        """
        Remove the element located at *index* from the list.

        Supports slicing.
        """
        del self._list[index]

    def __getitem__(self, index):
        """
        Return the element at position *index*.

        Supports slicing.
        """
        if isinstance(index, slice):
            return list(tup.value for tup in self._list[index])
        else:
            return self._list[index].value

    def __setitem__(self, index, value):
        """
        Replace the item at position *index* with *value*.

        Supports slicing.
        """
        _key = self._key
        if isinstance(index, slice):
            self._list[index] = list(Pair(_key(val), val) for val in value)
        else:
            self._list[index] = Pair(_key(value), value)

    def __iter__(self):
        """Create an iterator over the list."""
        return iter(tup.value for tup in iter(self._list))

    def __reversed__(self):
        """Create an iterator to traverse the list in reverse."""
        return iter(tup.value for tup in reversed(self._list))

    def __len__(self):
        """Return the number of elements in the list."""
        return len(self._list)

    def bisect_left(self, value):
        """
        Similar to the *bisect* module in the standard library, this returns an
        appropriate index to insert *value*. If *value* is already present, the
        insertion point will be before (to the left of) any existing entries.
        """
        return self._list.bisect_left(Pair(self._key(value), value))

    def bisect(self, value):
        """Same as bisect_right."""
        return self._list.bisect_right(Pair(self._key(value), value))

    def bisect_right(self, value):
        """
        Same as *bisect_left*, but if *value* is already present, the insertion
        point will be after (to the right of) any existing entries.
        """
        return self._list.bisect_right(Pair(self._key(value), value))

    def count(self, value):
        """Return the number of occurrences of *value* in the list."""
        _list = self._list
        _key = self._key(value)
        _pair = Pair(_key, value)

        _maxes = _list._maxes

        if not _maxes:
            return 0

        pos = bisect_left(_maxes, _pair)

        if pos == len(_maxes):
            return 0

        _lists = _list._lists

        idx = bisect_left(_lists[pos], _pair)

        total = 0
        len_lists = len(_lists)
        len_sublist = len(_lists[pos])

        while True:
            pair = _lists[pos][idx]
            if _key != pair.key:
                return total
            if value == pair.value:
                total += 1
            idx += 1
            if idx == len_sublist:
                pos += 1
                if pos == len_lists:
                    return total
                len_sublist = len(_lists[pos])
                idx = 0

    def copy(self):
        """Return a shallow copy of the sorted list with key."""
        return SortedListWithKey(self, key=self._key, load=self._load)

    __copy__ = copy

    def append(self, value):
        """
        Append the element *value* to the list. Raises a ValueError if the
        *value* would violate the sort order.
        """
        self._list.append(Pair(self._key(value), value))

    def extend(self, iterable):
        """
        Extend the list by appending all elements from *iterable*. Raises a
        ValueError if the sort order would be violated.
        """
        _key = self._key
        self._list.extend(Pair(_key(val), val) for val in iterable)

    def insert(self, index, value):
        """
        Insert the element *value* into the list at *index*. Raises a ValueError
        if the *value* at *index* would violate the sort order.
        """
        self._list.insert(index, Pair(self._key(value), value))

    def pop(self, index=-1):
        """
        Remove and return item at *index* (default last).  Raises IndexError if
        list is empty or index is out of range.  Negative indices are supported,
        as for slice indices.
        """
        return self._list.pop(index).value

    def index(self, value, start=None, stop=None):
        """
        Return the smallest *k* such that L[k] == value and i <= k < j`.  Raises
        ValueError if *value* is not present.  *stop* defaults to the end of the
        list. *start* defaults to the beginning. Negative indices are supported,
        as for slice indices.
        """
        _list = self._list
        _key = self._key(value)
        _pair = Pair(_key, value)
        _len = _list._len

        if start is None:
            start = 0
        if start < 0:
            start += _len
        if start < 0:
            start = 0

        if stop is None:
            stop = _len
        if stop < 0:
            stop += _len
        if stop > _len:
            stop = _len

        if stop <= start:
            raise ValueError('{0} is not in list'.format(repr(value)))

        _maxes = _list._maxes
        pos = bisect_left(_maxes, _pair)

        if pos == len(_maxes):
            raise ValueError('{0} is not in list'.format(repr(value)))

        _lists = _list._lists

        idx = bisect_left(_lists[pos], _pair)

        len_lists = len(_lists)
        len_sublist = len(_lists[pos])

        while True:
            pair = _lists[pos][idx]
            if _key != pair.key:
                raise ValueError('{0} is not in list'.format(repr(value)))
            if value == pair.value:
                loc = _list._loc(pos, idx)
                if start <= loc < stop:
                    return loc
            idx += 1
            if idx == len_sublist:
                pos += 1
                if pos == len_lists:
                    raise ValueError('{0} is not in list'.format(repr(value)))
                len_sublist = len(_lists[pos])
                idx = 0

    def as_list(self):
        """Very efficiently convert the SortedListWithKey to a list."""
        return list(tup.value for tup in self._list.as_list())

    def __add__(self, that):
        """
        Return a new sorted list containing all the elements in *self* and
        *that*. Elements in *that* do not need to be properly ordered with
        respect to *self*.
        """
        result = SortedListWithKey(key=self._key, load=self._load)
        values = self.as_list()
        values.extend(that)
        result.update(values)
        return result

    def __iadd__(self, that):
        """
        Update *self* to include all values in *that*. Elements in *that* do not
        need to be properly ordered with respect to *self*.
        """
        self.update(that)
        return self

    def __mul__(self, that):
        """
        Return a new sorted list containing *that* shallow copies of each item
        in SortedList.
        """
        values = self.as_list() * that
        return SortedListWithKey(values, key=self._key, load=self._load)

    def __imul__(self, that):
        """
        Increase the length of the list by appending *that* shallow copies of
        each item.
        """
        values = self.as_list() * that
        self.clear()
        self.update(values)
        return self

    def __eq__(self, that):
        """Compare two iterables for equality."""
        return ((len(self) == len(that))
                and all(lhs == rhs for lhs, rhs in zip(self, that)))

    def __ne__(self, that):
        """Compare two iterables for inequality."""
        return ((len(self) != len(that))
                or any(lhs != rhs for lhs, rhs in zip(self, that)))

    def __lt__(self, that):
        """Compare two iterables for less than."""
        return ((len(self) <= len(that))
                and all(lhs < rhs for lhs, rhs in zip(self, that)))

    def __le__(self, that):
        """Compare two iterables for less than equal."""
        return ((len(self) <= len(that))
                and all(lhs <= rhs for lhs, rhs in zip(self, that)))

    def __gt__(self, that):
        """Compare two iterables for greater than."""
        return ((len(self) >= len(that))
                and all(lhs > rhs for lhs, rhs in zip(self, that)))

    def __ge__(self, that):
        """Compare two iterables for greater than equal."""
        return ((len(self) >= len(that))
                and all(lhs >= rhs for lhs, rhs in zip(self, that)))

    @recursive_repr
    def __repr__(self):
        """Return string representation of SortedListWithKey."""
        temp = '{0}({1}, key={2}, load={3})'
        return temp.format(
            self.__class__.__name__,
            repr(self.as_list()),
            repr(self._key),
            repr(self._load)
        )

    def _check(self):
        _list, _key = self._list, self._key
        _list._check()
        assert all(pair.key == _key(pair.value) for pair in _list)
