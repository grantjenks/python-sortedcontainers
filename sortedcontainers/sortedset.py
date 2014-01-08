"""
Sorted set implementation.
"""

from sortedlist import SortedList
from collections import MutableSet, Sequence
from itertools import izip

class SortedSet(MutableSet, Sequence):
    def __init__(self, iterable=None, load=100):
        self._slist = SortedList(iterable, load)
        if iterable is not None:
            self.update(iterable)
    def __contains__(self, value):
        return (value in self._slist)
    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step, indices = self._slist._slice_indices(index)
            return SortedSet(self._slist[index] for index in indices)
        else:
            return self._slist[index]
    def __delitem__(self, index):
        del self._slist[index]
    def __setitem__(self, index, value):
        self._slist[index] = value
    def __eq__(self, that):
        if len(self) != len(that): return False
        if isinstance(that, SortedSet):
            return all(lhs == rhs for lhs, rhs in izip(self, that))
        else:
            return all((val in self) for val in that)
    def __ne__(self, that):
        if len(self) != len(that): return True
        if isinstance(that, SortedSet):
            return any(lhs != rhs for lhs, rhs in izip(self, that))
        else:
            return any((val not in self) for val in that)
    def __lt__(self, that):
        return ((len(self._slist) < len(that))
                and all((value in that) for value in self._slist))
    def __gt__(self, that):
        return ((len(self._slist) > len(that))
                and all((value in self._slist) for value in that))
    def __lte__(self, that):
        return all((value in that) for value in self._slist)
    def __gte__(self, that):
        return all((value in self._slist) for value in that)
    def __iter__(self):
        return iter(self._slist)
    def __len__(self):
        return len(self._slist)
    def reversed(self):
        return reversed(self._slist)
    def add(self, value):
        if value not in self._slist:
            self._slist.add(value)
    def bisect_left(self, value):
        return self._slist.bisect_left(value)
    def bisect(self, value):
        return self._slist.bisect(value)
    def bisect_right(self, value):
        return self._slist.bisect_right(value)
    def clear(self):
        self._slist.clear()
    def copy(self):
        return SortedSet(self._slist)
    def count(self, value):
        return self._slist.count(value)
    def difference(self, *iterables):
        new_set = self.copy()
        new_set.difference_update(*iterables)
        return new_set
    def difference_update(self, *iterables):
        for iterable in iterables:
            for value in iterable:
                self.discard(value)
    def discard(self, value):
        self._slist.discard(value)
    def index(self, value, start=None, stop=None):
        return self._slist.index(value, start, stop)
    def intersection(self, *iterables):
        new_set = self.copy()
        new_set.intersection_update(*iterables)
        return new_set
    def intersection_update(self, *iterables):
        new_list = SortedList()
        for iterable in iterables:
            for value in iterable:
                if value in self._slist:
                    if value not in new_list:
                        new_list.add(value)
            self._slist = new_list
            new_list = SortedList()
    def isdisjoint(self, that):
        return not any((value in self._slist) for value in that)
    def issubset(self, that):
        return all((value in that) for value in self._slist)
    def issuperset(self, that):
        return all((value in self._slist) for value in that)
    def symmetric_difference(self, that):
        new_set = self.copy()
        new_set.symmetric_difference_update(that)
        return new_set
    def symmetric_difference_update(self, that):
        new_list = SortedList()
        for value in self:
            if value not in that:
                new_list.add(value)
        for value in that:
            if value not in self:
                new_list.add(value)
        self._slist = new_list
    def pop(self, index=-1):
        return self._slist.pop(index)
    def remove(self, value):
        self._slist.remove(value)
    def union(self, *iterables):
        new_set = self.copy()
        new_set.update(*iterables)
        return new_set
    def update(self, *iterables):
        for iterable in iterables:
            for value in iterable:
                if value not in self._slist:
                    self._slist.add(value)
    def __repr__(self):
        reprs = (repr(value) for value in self)
        return 'SortedSet([{}])'.format(', '.join(reprs))
    def _check(self):
        self._slist._check()
        assert all(self[pos - 1] != self[pos]
                   for pos in xrange(1, len(self)))
