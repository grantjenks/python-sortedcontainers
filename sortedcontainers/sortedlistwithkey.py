# -*- coding: utf-8 -*-
#
# Sorted list with key implementation.

from sys import hexversion

from .sortedlist import SortedList
from collections import MutableSequence
from itertools import chain

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
    def __getitem__(self, index):
        return self.key if index == 0 else self.value
    def __repr__(self):
        return 'Pair({0}, {1})'.format(repr(self.key), repr(self.value))

class SortedListWithKey(MutableSequence):
    def __init__(self, iterable=None, key=lambda val: val, value_orderable=True, load=100):
        self._key = key
        self._list = SortedList(load=load)
        self._ordered = value_orderable

        if value_orderable:
            self._pair = lambda key, value: (key, value)
        else:
            self._pair = Pair

        if iterable is not None:
            self.update(iterable)

    def clear(self):
        self._list.clear()

    def add(self, value):
        pair = self._pair(self._key(value), value)
        self._list.add(pair)

    def update(self, iterable):
        _key, _pair = self._key, self._pair
        self._list.update(_pair(_key(val), val) for val in iterable)

    def _iter(self, pair):
        _list = self._list

        start = _list.bisect_left(pair)
        end = _list.bisect_right(pair)

        yield start

        if start == end:
            return

        start_pos, start_idx = _list._pos(start)
        end_pos, end_idx = _list._pos(end - 1)

        _lists = _list._lists
        segments = (_lists[pos] for pos in range(start_pos, end_pos + 1))
        iterator = chain.from_iterable(segments)

        # Advance the iterator to the start of the items.

        for rpt in range(start_idx):
            next(iterator)

        for rpt in range(end - start + 1):
            yield next(iterator)

    def __contains__(self, value):
        pair = self._pair(self._key(value), value)

        if self._ordered:
            return pair in self._list

        iterator = self._iter(pair)
        next(iterator)

        for duo in iterator:
            if value == duo[1]:
                return True
        else:
            return False

    def discard(self, value):
        pair = self._pair(self._key(value), value)

        if self._ordered:
            self._list.discard(pair)
            return

        iterator = self._iter(pair)
        start = next(iterator)

        for offset, duo in enumerate(iterator):
            if value == duo[1]:
                del self._list[start + offset]
                return

    def remove(self, value):
        pair = self._pair(self._key(value), value)

        if self._ordered:
            self._list.remove(pair)
            return

        iterator = self._iter(pair)
        start = next(iterator)

        for offset, duo in enumerate(iterator):
            if value == duo[1]:
                del self._list[start + offset]
                return
        else:
            raise ValueError

    def __delitem__(self, index):
        del self._list[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(tup[1] for tup in self._list[index])
        else:
            return self._list[index][1]

    def __setitem__(self, index, value):
        _key, _pair = self._key, self._pair
        if isinstance(index, slice):
            self._list[index] = list(_pair(_key(val), val) for val in value)
        else:
            self._list[index] = _pair(_key(value), value)

    def __iter__(self):
        return iter(tup[1] for tup in iter(self._list))

    def __reversed__(self):
        return iter(tup[1] for tup in reversed(self._list))

    def __len__(self):
        return len(self._list)

    def bisect_left(self, value):
        pair = self._pair(self._key(value), value)
        return self._list.bisect_left(pair)

    def bisect(self, value):
        pair = self._pair(self._key(value), value)
        return self._list.bisect(pair)

    def bisect_right(self, value):
        pair = self._pair(self._key(value), value)
        return self._list.bisect_right(pair)

    def count(self, value):
        pair = self._pair(self._key(value), value)

        if self._ordered:
            return self._list.count(pair)

        iterator = self._iter(pair)
        next(iterator)

        return sum(1 for duo in iterator if duo[1] == value)

    def append(self, value):
        pair = self._pair(self._key(value), value)
        self._list.append(pair)

    def extend(self, iterable):
        _key, _pair = self._key, self._pair
        self._list.extend(_pair(_key(val), val) for val in iterable)

    def insert(self, index, value):
        pair = self._pair(self._key(value), value)
        self._list.insert(index, pair)

    def pop(self, index=-1):
        return self._list.pop(index)[1]

    def index(self, value, start=None, stop=None):
        pair = self._pair(self._key(value), value)

        if self._ordered:
            return self._list.index(pair, start, stop)

        _len = self._list._len

        if start == None:
            start = 0
        if start < 0:
            start += _len
        if start < 0:
            start = 0

        if stop == None:
            stop = _len
        if stop < 0:
            stop += _len
        if stop > _len:
            stop = _len

        if stop <= start:
            raise ValueError

        iterator = self._iter(pair)
        begin = next(iterator)

        for offset, val in enumerate(iterator):
            if value == val[2] and start <= (begin + offset) < stop:
                return begin + offset
        else:
            raise ValueError

    def as_list(self):
        return list(tup[1] for tup in self._list.as_list())

    def __add__(self, that):
        result = SortedListWithKey(
            key=self._key,
            value_orderable=self._ordered,
            load=self._list._load
        )
        values = self.as_list()
        values.extend(that)
        result.update(values)
        return result

    def __iadd__(self, that):
        self.update(that)
        return self

    def __mul__(self, that):
        values = self.as_list() * that
        return SortedListWithKey(
            values, 
            key=self._key,
            value_orderable=self._ordered,
            load=self._list._load
        )

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
        temp = 'SortedListWithKey({0}, key={1}, value_orderable={2}, load={3})'
        return temp.format(
            repr(self.as_list()),
            repr(self._key),
            repr(self._ordered),
            repr(self._list._load)
        )

    def _check(self):
        _list, _key = self._list, self._key
        _list._check()
        assert all(pair[0] == _key(pair[1]) for pair in _list)
