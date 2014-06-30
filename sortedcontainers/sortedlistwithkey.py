# -*- coding: utf-8 -*-
#
# Sorted list with key implementation.

from .sortedlist import SortedList
from collections import MutableSequence

class SortedListWithKey(MutableSequence):
    def __init__(self, iterable=None, key=lambda val: val, load=100):
        self.key = key
        self._list = SortedList(load=load)

        if iterable is not None:
            self.update(iterable)

    def clear(self):
        self._list.clear()

    def add(self, value):
        pair = (self.key(value), value)
        self._list.add(pair)

    def update(self, iterable):
        self._list.update((self.key(val), val) for val in iterable)

    def __contains__(self, value):
        pair = (self.key(value), value)
        return pair in self._list

    def discard(self, value):
        pair = (self.key(value), value)
        self._list.discard(pair)

    def remove(self, value):
        pair = (self.key(value), value)
        self._list.remove(pair)

    def __delitem__(self, index):
        del self._list[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(tup[1] for tup in self._list[index])
        else:
            return self._list[index][1]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            self._list[index] = list((self.key(val), val) for val in value)
        else:
            self._list[index] = (self.key(value), value)

    def __iter__(self):
        return iter(tup[1] for tup in iter(self._list))

    def __reversed__(self):
        return iter(tup[1] for tup in reversed(self._list))

    def __len__(self):
        return len(self._list)

    def bisect_left(self, value):
        pair = (self.key(value), value)
        return self._list.bisect_left(pair)

    def bisect(self, value):
        pair = (self.key(value), value)
        return self._list.bisect(pair)

    def bisect_right(self, value):
        pair = (self.key(value), value)
        return self._list.bisect_right(pair)

    def count(self, value):
        pair = (self.key(value), value)
        return self._list.count(pair)

    def append(self, value):
        pair = (self.key(value), value)
        self._list.append(pair)

    def extend(self, iterable):
        self._list.extend((self.key(val), val) for val in iterable)

    def insert(self, index, value):
        pair = (self.key(value), value)
        self._list.insert(index, pair)

    def pop(self, index=-1):
        return self._list.pop(index)[1]

    def index(self, value, start=None, stop=None):
        pair = (self.key(value), value)
        return self._list.index(pair, start, stop)

    def as_list(self):
        return list(tup[1] for tup in self._list.as_list())

    def __add__(self, that):
        result = SortedListWithKey(key=self.key)
        result.update(self)
        result.update(that)
        return result

    def __iadd__(self, that):
        self.update(that)
        return self

    def __mul__(self, that):
        values = self.as_list() * that
        return SortedListWithKey(values, key=self.key)

    def __imul__(self, that):
        values = self.as_list() * that
        self.clear()
        self.update(values)
        return self

    def __eq__(self, that):
        return ((len(self) == len(that))
                and all(lhs == rhs for lhs, rhs in zip(self, that)))

    def __ne__(self, that):
        return ((len(self) != len(that))
                or any(lhs != rhs for lhs, rhs in zip(self, that)))

    def __lt__(self, that):
        return ((len(self) <= len(that))
                and all(lhs < rhs for lhs, rhs in zip(self, that)))

    def __le__(self, that):
        return ((len(self) <= len(that))
                and all(lhs <= rhs for lhs, rhs in zip(self, that)))

    def __gt__(self, that):
        return ((len(self) >= len(that))
                and all(lhs > rhs for lhs, rhs in zip(self, that)))

    def __ge__(self, that):
        return ((len(self) >= len(that))
                and all(lhs >= rhs for lhs, rhs in zip(self, that)))

    def __repr__(self):
        return 'SortedListWithKey({0}, key={1})'.format(
            repr(self.as_list()), repr(self.key))

    def _check(self):
        self._list._check()
        for key, value in self._list:
            assert self.key(value) == key
