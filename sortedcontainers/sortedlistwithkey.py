# -*- coding: utf-8 -*-
#
# Sorted list with key implementation.

from sys import hexversion
from .sortedlist import SortedList, recursive_repr
from collections import MutableSequence
from itertools import chain
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
    def __getitem__(self, index):
        return self.key if index == 0 else self.value
    @recursive_repr
    def __repr__(self):
        return 'Pair({0}, {1})'.format(repr(self.key), repr(self.value))

class SortedListWithKey(MutableSequence):
    def __init__(self, iterable=None, key=lambda val: val, value_orderable=True, load=1000):
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

    def __contains__(self, value):
        _list = self._list
        _key =  self._key(value)
        _pair = self._pair(_key, value)

        if self._ordered:
            return _pair in _list

        _maxes = _list._maxes

        if _maxes is None:
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
        _list = self._list
        _key =  self._key(value)
        _pair = self._pair(_key, value)

        if self._ordered:
            _list.discard(_pair)
            return

        _maxes = _list._maxes

        if _maxes is None:
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
        _list = self._list
        _key =  self._key(value)
        _pair = self._pair(_key, value)

        if self._ordered:
            _list.remove(_pair)
            return

        _maxes = _list._maxes

        if _maxes is None:
            raise ValueError

        pos = bisect_left(_maxes, _pair)

        if pos == len(_maxes):
            raise ValueError

        _lists = _list._lists

        idx = bisect_left(_lists[pos], _pair)

        len_lists = len(_lists)
        len_sublist = len(_lists[pos])

        while True:
            pair = _lists[pos][idx]
            if _key != pair.key:
                raise ValueError
            if value == pair.value:
                _list._delete(pos, idx)
                return
            idx += 1
            if idx == len_sublist:
                pos += 1
                if pos == len_lists:
                    raise ValueError
                len_sublist = len(_lists[pos])
                idx = 0

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
        _list = self._list
        _key =  self._key(value)
        _pair = self._pair(_key, value)

        if self._ordered:
            return _list.count(_pair)

        _maxes = _list._maxes

        if _maxes is None:
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
        _key, _ordered, _load = self._key, self._ordered, self._list._load
        kwargs = dict(key=_key, value_orderable=_ordered, load=_load)
        return SortedListWithKey(self, **kwargs)

    def __copy__(self):
        """Return a shallow copy of the sorted list with key."""
        return self.copy()

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
        _list = self._list
        _key =  self._key(value)
        _pair = self._pair(_key, value)

        if self._ordered:
            return _list.index(_pair, start, stop)

        _len = _list._len

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

        _maxes = _list._maxes
        pos = bisect_left(_maxes, _pair)

        if pos == len(_maxes):
            raise ValueError

        _lists = _list._lists

        idx = bisect_left(_lists[pos], _pair)

        len_lists = len(_lists)
        len_sublist = len(_lists[pos])

        while True:
            pair = _lists[pos][idx]
            if _key != pair.key:
                raise ValueError
            if value == pair.value:
                loc = _list._loc(pos, idx)
                if start <= loc < stop:
                    return loc
            idx += 1
            if idx == len_sublist:
                pos += 1
                if pos == len_lists:
                    raise ValueError
                len_sublist = len(_lists[pos])
                idx = 0

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

    @recursive_repr
    def __repr__(self):
        temp = '{0}({1}, key={2}, value_orderable={3}, load={4})'
        return temp.format(
            self.__class__.__name__,
            repr(self.as_list()),
            repr(self._key),
            repr(self._ordered),
            repr(self._list._load)
        )

    def _check(self):
        _list, _key = self._list, self._key
        _list._check()
        assert all(pair[0] == _key(pair[1]) for pair in _list)
