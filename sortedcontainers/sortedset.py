"""
Sorted set implementation.
"""

from sortedlist import SortedList
from itertools import groupby

class SortedSet():
    def __init__(self, iterable=None, load=100):
        if iterable is not None:
            iterable = (value[0] for value in groupby(sorted(iterable)))
        self._slist = SortedList(iterable, load)
    def __contains__(self, value):
        return (value in self._slist)
    def __delitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError
        else:
            del self._slist[index]
    def __lt__(self, that):
        # todo: is it valid to use equality?
        # check length!
        return (all((value in that) for value in self._slist)
                and (self._slist != that))
    def __gt__(self, that):
        # todo: is it valid to use equality?
        return (all((value in self._slist) for value in that)
                and (self._slist != that))
    def __getitem__(self, index):
        if isinstance(index, slice):
            # Returns a SortedSet
            raise NotImplementedError
        else:
            return self._slist[index]
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
        return SortedSet(self)
    def count(self, value):
        return self._slist.count(value)
    def difference(self, *iterables):
        new_set = SortedSet(self)
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
        new_set = SortedSet(self)
        new_set.intersection_update(*iterables)
        return new_set
    def intersection_update(self, *iterables):
        new_list = SortedList()
        for iterable in iterables:
            for value in iterable:
                if value in self._slist:
                    new_list.add(value)
        self._slist = new_list
    def isdisjoint(self, that):
        return not any((value in self._slist) for value in that)
    def issubset(self, that):
        return all((value in that) for value in self._slist)
    def issuperset(self, that):
        return all((value in self._slist) for value in that)
    def symmetric_difference(self, that):
        new_set = SortedSet(self)
        new_set.symmetric_difference_update(that)
        return new_set
    def symmetric_difference_update(self, that):
        raise NotImplementedError
