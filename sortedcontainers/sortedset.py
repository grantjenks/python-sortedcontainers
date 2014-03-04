"""
Sorted set implementation.
"""

from sys import version_info

from .sortedlist import SortedList
from collections import MutableSet, Sequence
from itertools import chain

if version_info[0] == 2:
    from itertools import izip as zip

class SortedSet(MutableSet, Sequence):
    def __init__(self, iterable=None, load=100, _set=None):
        self._set = set() if _set is None else _set
        self._list = SortedList(self._set, load=load)
        if iterable is not None:
            self.update(iterable)
    def __contains__(self, value):
        return (value in self._set)
    def __getitem__(self, index):
        if isinstance(index, slice):
            return SortedSet(self._list[index])
        else:
            return self._list[index]
    def __delitem__(self, index):
        if isinstance(index, slice):
            values = self._list[index]
            self._set.difference_update(values)
        else:
            value = self._list[index]
            self._set.remove(value)
        del self._list[index]
    def __setitem__(self, index, value):
        if isinstance(index, slice):
            values = self._list[index]
            self._set.difference_update(values)
            self._set.update(value)
        else:
            value = self._list[index]
            self._set.remove(value)
            self._set.add(value)
        self._list[index] = value
    def __eq__(self, that):
        if len(self) != len(that):
            return False
        if isinstance(that, SortedSet):
            return all(lhs == rhs for lhs, rhs in zip(self, that))
        elif isinstance(that, set):
            return (self._set == that)
        else:
            return all(val in self._set for val in that)
    def __ne__(self, that):
        if len(self) != len(that):
            return True
        if isinstance(that, SortedSet):
            return any(lhs != rhs for lhs, rhs in zip(self, that))
        elif isinstance(that, set):
            return (self._set != that)
        else:
            return any(val not in self._set for val in that)
    def __lt__(self, that):
        if isinstance(that, set):
            return (self._set < that)
        else:
            return (len(self) < len(that)) and all(val in that for val in self._list)
    def __gt__(self, that):
        if isinstance(that, set):
            return (self._set > that)
        else:
            return (len(self) > len(that)) and all(val in self._set for val in that)
    def __le__(self, that):
        if isinstance(that, set):
            return (self._set <= that)
        else:
            return all(val in that for val in self._list)
    def __ge__(self, that):
        if isinstance(that, set):
            return (self._set >= that)
        else:
            return all(val in self._set for val in that)
    def __and__(self, that):
        return self.intersection(that)
    def __or__(self, that):
        return self.union(that)
    def __sub__(self, that):
        return self.difference(that)
    def __xor__(self, that):
        return self.symmetric_difference(that)
    def __iter__(self):
        return iter(self._list)
    def __len__(self):
        return len(self._set)
    def __reversed__(self):
        return reversed(self._list)
    def add(self, value):
        if value not in self._set:
            self._set.add(value)
            self._list.add(value)
    def bisect_left(self, value):
        return self._list.bisect_left(value)
    def bisect(self, value):
        return self._list.bisect(value)
    def bisect_right(self, value):
        return self._list.bisect_right(value)
    def clear(self):
        self._set.clear()
        self._list.clear()
    def copy(self):
        new_set = SortedSet()
        new_set._set = self._set
        new_set._list = self._list
        return new_set
    def count(self, value):
        return 1 if value in self._set else 0
    def discard(self, value):
        if value in self._set:
            self._set.remove(value)
            self._list.discard(value)
    def index(self, value, start=None, stop=None):
        return self._list.index(value, start, stop)
    def isdisjoint(self, that):
        return self._set.isdisjoint(that)
    def issubset(self, that):
        return self._set.issubset(that)
    def issuperset(self, that):
        return self._set.issuperset(that)
    def pop(self, index=-1):
        value = self._list.pop(index)
        self._set.remove(value)
        return value
    def remove(self, value):
        self._set.remove(value)
        self._list.remove(value)
    def difference(self, *iterables):
        diff = self._set.difference(*iterables)
        new_set = SortedSet(load=self._list._load, _set=diff)
        return new_set
    def difference_update(self, *iterables):
        values = set(chain(*iterables))
        if (4 * len(values)) > len(self):
            self._set.difference_update(values)
            self._list.clear()
            self._list.update(self._set)
        else:
            for value in values:
                self.discard(value)
    def intersection(self, *iterables):
        comb = self._set.intersection(*iterables)
        new_set = SortedSet(load=self._list._load, _set=comb)
        return new_set
    def intersection_update(self, *iterables):
        self._set.intersection_update(*iterables)
        self._list.clear()
        self._list.update(self._set)
    def symmetric_difference(self, that):
        diff = self._set.symmetric_difference(that)
        new_set = SortedSet(load=self._list._load, _set=diff)
        return new_set
    def symmetric_difference_update(self, that):
        self._set.symmetric_difference_update(that)
        self._list.clear()
        self._list.update(self._set)
    def union(self, *iterables):
        return SortedSet(chain(iter(self), *iterables), load=self._list._load)
    def update(self, *iterables):
        """Update sorted set with iterables."""
        values = set(chain(*iterables))
        if (4 * len(values)) > len(self):
            self._set.update(values)
            self._list.clear()
            self._list.update(self._set)
        else:
            for value in values:
                self.add(value)
    def __repr__(self):
        return 'SortedSet({0})'.format(repr(list(self)))
    def _check(self):
        self._list._check()
        assert len(self._set) == len(self._list)
        assert all(val in self._set for val in self._list)
