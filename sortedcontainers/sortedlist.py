"""
Sorted list implementation.
"""

from bisect import bisect_left, bisect_right, insort
from itertools import chain, izip, imap
from collections import MutableSequence
from operator import iadd

class SortedList(MutableSequence):
    def __init__(self, iterable=None, load=100):
        self.clear()
        self._load, self._twice, self._half = load, load * 2, load / 2

        if iterable is not None:
            self.update(iterable)

    def clear(self):
        self._len, self._maxes, self._lists, self._cumsum = 0, None, [], []

    def add(self, val):
        """Add a val to the sorted list."""
        if self._maxes is None:
            self._maxes = [val]
            self._lists = [[val]]
        else:
            pos = bisect_right(self._maxes, val)

            if pos == len(self._maxes):
                pos -= 1
                self._maxes[pos] = val
                self._lists[pos].append(val)
            else:
                insort(self._lists[pos], val)

            self._expand(pos)

        self._len += 1

    def _expand(self, pos):
        if len(self._lists[pos]) > self._twice:
            half = self._lists[pos][self._load:]
            self._lists[pos] = self._lists[pos][:self._load]
            self._maxes[pos] = self._lists[pos][-1]
            self._maxes.insert(pos + 1, half[-1])
            self._lists.insert(pos + 1, half)

    def update(self, iterable):
        """Update this sorted list with values from iterable."""
        values = sorted(iterable)

        if self._maxes is None and len(values) > 0:
            values.sort()
            self._lists = [values[pos:(pos + self._load)]
                          for pos in xrange(0, len(values), self._load)]
            self._maxes = [sublist[-1] for sublist in self._lists]
            self._len = len(values)
        else:
            for val in values:
                self.add(val)

    def __contains__(self, val):
        """Return True iff val in sorted list."""
        if self._maxes is None:
            return False

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return False

        index = bisect_left(self._lists[pos], val)

        return self._lists[pos][index] == val

    def discard(self, val):
        """Remove the first occurrence of val.
        If val is not a member, does nothing."""
        if self._maxes is None:
            return

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return

        index = bisect_left(self._lists[pos], val)

        if self._lists[pos][index] == val:
            self._delete(pos, index)

    def remove(self, val):
        """Remove the first occurrence of val.
        If val is not a member, raise ValueError."""
        if self._maxes is None:
            raise ValueError

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            raise ValueError

        index = bisect_left(self._lists[pos], val)

        if self._lists[pos][index] == val:
            self._delete(pos, index)
        else:
            raise ValueError

    def _delete(self, pos, index):
        """Delete the item at the given (pos, index).
        Combines lists that are less than half the load level."""
        del self._lists[pos][index]
        self._len -= 1

        if len(self._lists[pos]) == 0:
            del self._maxes[pos]
            del self._lists[pos]

            if len(self._maxes) == 0:
                self._maxes = None
                self._lists = []
        else:
            self._maxes[pos] = self._lists[pos][-1]

            if len(self._lists) > 1 and len(self._lists[pos]) < self._half:
                if pos == 0: pos += 1
                self._lists[pos - 1].extend(self._lists[pos])
                self._maxes[pos - 1] = self._lists[pos - 1][-1]
                del self._maxes[pos]
                del self._lists[pos]
                self._expand(pos - 1)

    def _index(self, pos, index):
        return index + sum(len(self._lists[idx]) for idx in xrange(pos))

    def _pos(self, index):
        if self._maxes is None:
            raise IndexError

        if index < 0:
            index += self._len
        if index < 0:
            raise IndexError
        if index >= self._len:
            raise IndexError

        for pos, sub_len in enumerate(imap(len, self._lists)):
            if index < sub_len:
                return pos, index
            else:
                index -= sub_len

    def __delitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError
        else:
            pos, index = self._pos(index)
            self._delete(pos, index)

    def __getitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError
        else:
            pos, index = self._pos(index)
            return self._lists[pos][index]

    def fast_getitem(self, index):
        # TODO: Change def _pos and def _index
        if self._maxes is None:
            raise IndexError

        if index < 0:
            index += self._len
        if index < 0:
            raise IndexError
        if index >= self._len:
            raise IndexError

        pos = bisect_right(self._cumsum, index)

        if pos == len(self._cumsum):
            if pos == 0:
                self._cumsum.append(len(self._lists[0]))
                pos += 1

            while self._cumsum[-1] < index:
                self._cumsum.append(self._cumsum[-1] + len(self._lists[pos]))
                pos += 1

            pos -= 1

        if pos == 0:
            return self._lists[pos][index]
        else:
            return self._lists[pos][index - self._cumsum[pos - 1]]

    def __setitem__(self, idx, val):
        if isinstance(idx, slice):
            raise NotImplementedError
        else:
            pos, index = self._pos(idx)

            if idx < 0: idx += self._len

            if idx > 0:
                index_prev = index - 1
                pos_prev = pos

                if index_prev < 0:
                    pos_prev -= 1
                    index_prev = len(self._lists[pos_prev]) - 1

                if self._lists[pos_prev][index_prev] > val:
                    raise ValueError

            if idx < (self._len - 1):
                index_next = index + 1
                pos_next = pos

                if index_next == len(self._lists[pos_next]):
                    pos_next += 1
                    index_next = 0

                if self._lists[pos_next][index_next] < val:
                    raise ValueError

            self._lists[pos][index] = val

    def __iter__(self):
        return chain.from_iterable(self._lists)

    def reversed(self):
        start = len(self._lists) - 1
        iterable = (reversed(self._lists[pos])
                    for pos in xrange(start, -1, -1))
        return chain.from_iterable(iterable)

    def __len__(self):
        return self._len

    def bisect_left(self, val):
        if self._maxes is None:
            return 0

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return self._index(pos, 0)

        index = bisect_left(self._lists[pos], val)

        return self._index(pos, index)

    def bisect(self, val):
        return self.bisect_left(val)

    def bisect_right(self, val):
        if self._maxes is None: return 0

        pos = bisect_right(self._maxes, val)

        if pos == len(self._maxes):
            return self._index(pos, 0)

        index = bisect_right(self._lists[pos], val)

        return self._index(pos, index)

    def count(self, val):
        if self._maxes is None:
            return 0

        start = bisect_left(self._maxes, val)
        right = bisect_right(self._maxes, val)

        if right < len(self._lists):
            right += 1

        return sum(self._lists[pos].count(val)
                   for pos in xrange(start, right))

    def append(self, val):
        """Append the given val to the end of the sorted list.
        Raises ValueError if the val would make the list unsorted.
        """
        if self._maxes is None:
            self._maxes = [val]
            self._lists = [[val]]
            self._len = 1
            return

        pos = len(self._lists) - 1

        if val < self._lists[pos][-1]:
            raise ValueError

        self._maxes[pos] = val
        self._lists[pos].append(val)
        self._len += 1

        self._expand(pos)

    def extend(self, values):
        """Extend this list with the given values.
        Raises ValueError if the values would make the list unsorted.
        """
        if not isinstance(values, list):
            values = list(values)

        if any(values[pos - 1] > values[pos]
               for pos in xrange(1, len(values))):
            raise ValueError

        offset = 0

        if self._maxes is None:
            self._maxes = []
            self._lists = []
        else:
            if values[0] < self._lists[-1][-1]:
                raise ValueError

            if len(self._lists[-1]) < self._half:
                self._lists[-1].extend(values[:self._load])
                self._maxes[-1] = self._lists[-1][-1]
                offset = self._load

        for idx in xrange(offset, len(values), self._load):
            self._lists.append(values[idx:(idx + self._load)])
            self._maxes.append(self._lists[-1][-1])

        self._len += len(values)

    def insert(self, index, val):
        """Insert the given val at index.
        Raise ValueError if the val at index would make the list unsorted.
        """
        if index < 0:
            index += self._len
        if index < 0:
            index = 0
        if index > self._len:
            index = self._len

        if self._maxes is None:
            # The index must be zero by the inequalities above.
            self._maxes = [val]
            self._lists = [[val]]
            self._len = 1
            return

        if index == 0:
            if val > self._lists[0][0]:
                raise ValueError
            else:
                self._lists[0].insert(0, val)
                self._expand(0)
                self._len += 1
                return

        if index == self._len:
            pos = len(self._lists) - 1
            if self._lists[pos][-1] > val:
                raise ValueError
            else:
                self._lists[pos].append(val)
                self._maxes[pos] = self._lists[pos][-1]
                self._expand(pos)
                self._len += 1
                return

        pos, index = self._pos(index)
        index_before = index - 1
        if index_before < 0:
            pos_before = pos - 1
            index_before = len(self._lists[pos_before]) - 1
        else:
            pos_before = pos

        before = self._lists[pos_before][index_before]
        if before <= val <= self._lists[pos][index]:
            self._lists[pos].insert(index, val)
            self._expand(pos)
            self._len += 1
        else:
            raise ValueError

    def pop(self, index=-1):
        if index < 0:
            index += self._len
        if index < 0 or index >= self._len:
            raise IndexError

        pos, index = self._pos(index)
        val = self._lists[pos][index]
        self._delete(pos, index)

        return val

    def index(self, val, start=None, stop=None):
        if self._maxes is None:
            raise ValueError

        if start == None:
            start = 0
        if start < 0:
            start += self._len
        if start < 0:
            start = 0

        if stop == None:
            stop = self._len
        if stop < 0:
            stop += self._len
        if stop > self._len:
            stop = self._len

        if stop <= start:
            raise ValueError

        stop -= 1

        left = self.bisect_left(val)

        if (left == self._len) or (self[left] != val):
            raise ValueError

        right = self.bisect_right(val) - 1

        pos = max(start, left)

        if pos <= right and pos <= stop:
            return pos

        raise ValueError

    def as_list(self):
        return reduce(iadd, self._lists, [])

    def __add__(self, that):
        values = self.as_list()
        values.extend(that)
        return SortedList(values)

    def __iadd__(self, that):
        self.update(that)
        return self

    def __mul__(self, that):
        values = self.as_list() * that
        return SortedList(values)

    def __imul__(self, that):
        values = self.as_list() * that
        self.clear()
        self.update(values)
        return self

    def __eq__(self, that):
        return ((self._len == len(that))
                and all(lhs == rhs for lhs, rhs in izip(self, that)))

    def __ne__(self, that):
        return ((self._len != len(that))
                or any(lhs != rhs for lhs, rhs in izip(self, that)))

    def __lt__(self, that):
        return ((self._len <= len(that))
                and all(lhs < rhs for lhs, rhs in izip(self, that)))

    def __le__(self, that):
        return ((self._len <= len(that))
                and all(lhs <= rhs for lhs, rhs in izip(self, that)))

    def __gt__(self, that):
        return ((self._len >= len(that))
                and all(lhs > rhs for lhs, rhs in izip(self, that)))

    def __ge__(self, that):
        return ((self._len >= len(that))
                and all(lhs >= rhs for lhs, rhs in izip(self, that)))

    def __repr__(self):
        reprs = (repr(value) for value in self)
        return 'SortedList([{}])'.format(', '.join(reprs))

    def _check(self):
        try:
            # Check load parameters.

            assert self._load >= 4
            assert self._half == (self._load / 2)
            assert self._twice == (self._load * 2)

            # Check empty sorted list case.

            if self._maxes is None:
                assert self._lists == []
                return

            assert len(self._maxes) > 0 and len(self._lists) > 0

            # Check all sublists are sorted.

            assert all(sublist[pos - 1] <= sublist[pos]
                       for sublist in self._lists
                       for pos in xrange(1, len(sublist)))

            # Check beginning/end of sublists are sorted.

            for pos in xrange(1, len(self._lists)):
                assert self._lists[pos - 1][-1] <= self._lists[pos][0]

            # Check length of _maxes and _lists match.

            assert len(self._maxes) == len(self._lists)

            # Check _maxes is a map of _lists.

            assert all(self._maxes[pos] == self._lists[pos][-1]
                       for pos in xrange(len(self._maxes)))

            # Check load level is less than _twice.

            assert all(len(sublist) <= self._twice for sublist in self._lists)

            # Check load level is greater than _half for all
            # but the last sublist.

            assert all(len(self._lists[pos]) >= self._half
                       for pos in xrange(0, len(self._lists) - 1))

            # Check length.

            assert self._len == sum(len(sublist) for sublist in self._lists)

        except AssertionError:
            import sys, traceback

            traceback.print_exc(file=sys.stdout)

            print self._len, self._load, self._half, self._twice
            print self._maxes
            print self._lists

            raise
