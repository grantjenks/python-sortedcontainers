"""
Sorted list implementation.

Missing:
* del L[i:j]
* L[i:j]
* L[i:j] = iterable
* testing
"""

import bisect
from functools import total_ordering
from itertools import chain, izip

@total_ordering
class SortedList:
    def __init__(self, iterable=None, load=1000):
        self.clear()
        self.load, self.twice, self.half = load, load * 2, load / 2

        if iterable is not None:
            self.update(iterable)

    def clear(self):
        self._len, self._maxes, self._lists = 0, None, None

    def add(self, val):
        """Add a val to the sorted list."""
        if self._maxes is None:
            self._maxes = [val]
            self._lists = [[val]]
        else:
            pos = bisect.bisect_right(self._maxes, val)

            if pos == len(self._maxes):
                pos -= 1
                self._maxes[pos] = val
                self._lists[pos].append(val)
            else:
                bisect.insort(self._lists[pos], val)

            self._grow(pos)

        self._len += 1

    def _expand(self, pos):
        if len(self._lists[pos]) > self.twice:
            half = self._lists[pos][self.load:]
            self._lists[pos] = self._lists[pos][:self.load]
            self._maxes[pos] = self._lists[pos][-1]
            self._maxes.insert(pos + 1, half[-1])
            self._lists.insert(pos + 1, half)

    def update(self, iterable):
        """Update this sorted list with values from iterable."""
        values = sorted(iterable)

        if self._maxes is None:
            self._lists = [values[pos:(pos + self.load)]
                          for pos in xrange(0, len(values), self.load)]
            self._maxes = [sublist[-1] for sublist in self._lists]
            self._len = len(values)
        else:
            for val in values:
                self.add(val)

    def __contains__(self, val):
        """Return True iff val in sorted list."""
        if self._maxes is None:
            return False

        pos = bisect.bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return False

        index = bisect.bisect_left(self._lists[pos], val)

        if index == len(self._lists[pos]):
            return False

        return self._lists[pos][index] == val

    def discard(self, val):
        """Remove the first occurrence of val.
        If val is not a member, does nothing."""
        if self._maxes is None:
            return

        pos = bisect.bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return

        index = bisect.bisect_left(self._lists[pos], val)

        if index == len(self._lists[pos]):
            return

        if self._lists[pos][index] == val:
            self._delete(pos, index)

    def remove(self, val):
        """Remove the first occurrence of val.
        If val is not a member, raise ValueError."""
        if self._maxes is None:
            raise ValueError

        pos = bisect.bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            raise ValueError

        index = bisect.bisect_left(self._lists[pos], val)

        if index == len(self._lists[pos]):
            raise ValueError

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
                self._lists = None
        else:
            self._maxes[pos] = self._lists[pos][-1]

            if len(self._lists) > 1 and len(self._lists[pos]) < self.half:
                if pos == 0: pos += 1
                self._lists[pos - 1].extend(self._lists[pos])
                del self._maxes[pos]
                del self._lists[pos]

    def _index(self, pos, index):
        return index + sum(len(self._lists[idx]) for idx in xrange(pos))

    def _pos(self, index):
        if self._maxes is None:
            raise IndexError

        for pos in xrange(len(self._maxes)):
            index -= len(self._lists[pos])
            if index < 0:
                break
        else:
            raise IndexError

        index += len(self._lists[pos])

        return pos, index

    def __delitem__(self, index):
        pos, index = self._pos(index)
        self._delete(pos, index)

    def __getitem__(self, index):
        pos, index = self._pos(index)
        return self._lists[pos][index]

    def __setitem__(self, idx, val):
        pos, index = self._pos(idx)
        self._lists[pos][index] = val

    def __iter__(self):
        return chain.from_iterable(self._lists)

    def reversed(self):
        return chain.from_iterable(reversed(map(reversed, self._lists)))

    def __len__(self):
        return self._len

    def bisect_left(self, val):
        if self._maxes is None:
            return 0

        pos = bisect.bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return self._index(pos, 0)

        index = bisect.bisect_left(self._lists[pos], val)

        return self._index(pos, index)

    def bisect(self, val):
        return self.bisect_left(val)

    def bisect_right(self, val):
        if self._maxes is None: return 0

        pos = bisect.bisect_right(self._maxes, val)

        if pos == len(self._maxes):
            return self._index(pos, 0)

        index = bisect.bisect_right(self._lists[pos], val)

        return self._index(pos, index)

    def count(self, val):
        if self._maxes is None:
            return 0

        start = bisect.bisect_left(self._maxes, val)
        right = bisect.bisect_right(self._maxes, val)

        if start == right:
            return self._lists[start].count(val)
        else:
            return sum(self._lists[pos].count(val)
                       for val in xrange(start, right))

        return total

    def append(self, val):
        """Append the given val to the end of the sorted list.
        Raises ValueError if the val would make the list unsorted.
        """
        if self._maxes is None:
            self._maxes = [val]
            self._lists = [[val]]
            return

        pos = len(self._lists) - 1

        if val < self._lists[pos][-1]:
            raise ValueError

        self._maxes[pos] = val
        self._lists[pos].append(val)

        self._expand(pos)

    def extend(self, values):
        """Extend this list with the given values.
        Raises ValueError if the values would make the list unsorted.
        """
        values = list(values)

        if any(values[pos - 1] > values[pos] for pos in xrange(1, len(values))):
            raise ValueError

        if self._maxes is None:
            self.update(values)
            return

        if values[0] < self._lists[-1][-1]:
            raise ValueError

        for value in values:
            self._maxes[-1] = value
            self._lists[-1].append(value)
            self._expand(len(self._lists) - 1)

    def insert(self, index, val):
        """Insert the given val at index.
        Raise ValueError if the val at index would make the list unsorted.
        """
        if index < 0:
            index += len(self)
        if index < 0:
            index = 0
        if index > self._len:
            index = self._len

        if self._maxes is None:
            if index == 0:
                self._maxes = [val]
                self._lists = [[val]]
                return
            else:
                raise ValueError

        if index == 0:
            if val > self._lists[0][0]:
                raise ValueError
            else:
                self._lists[0].insert(0, val)
                self._expand(0)
                return

        pos, index = self._pos(index)
        index_before = index - 1
        if index_before < 0:
            pos_before = pos - 1
            index_before = len(self._lists[pos_before]) - 1
        else:
            pos_before = pos

        before = self.lists[pos_before][index_before]
        if before <= val <= self.lists[pos][index]:
            self.lists[pos].insert(index, val)
            self._expand(pos)
        else:
            raise ValueError

    def pop(self, index=-1):
        if index < 0:
            index += len(self)
        if index < 0 or index >= self._len:
            raise IndexError

        pos, index = self._index(index)
        val = self._lists[pos][index]

        self._delete(pos, index)

        return val

    def index(self, val, start=0, stop=-1):
        if self._maxes is None:
            raise ValueError

        if start < 0:
            start += len(self)
        if start < 0:
            start = 0
        if start > self._len:
            start = self._len

        if stop < 0:
            stop += len(self)
        if stop < 0:
            stop = 0
        if stop > self._len:
            stop = self._len

        pos = bisect.bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            raise ValueError

        index = bisect.bisect_left(self._lists[pos], val)

        if index == len(self._lists[pos]):
            raise ValueError

        start = self._pos(start)
        stop = self._pos(stop)

        while self._lists[pos][index] == val:
            if start <= (pos, index) < stop:
                return self._index(pos, index)
            else:
                index += 1
                if index == len(self._lists[pos]):
                    index = 0
                    pos += 1

        raise ValueError

    def __mul__(self, that):
        values = list(self)
        values *= that
        return SortedList(values)

    def __imul__(self, that):
        values = list(self)
        self.clear()
        values *= that
        self.update(values)

    def __eq__(self, that):
        if len(self) != len(that):
            return False
        return all(lhs == rhs for lhs, rhs in izip(self, that))

    def __lt__(self, that):
        it_self, it_that = iter(self), iter(that)
        lhs_stop, rhs_stop = False, False

        while True:
            try:
                lhs = it_self.next()
            except StopIteration:
                lhs_stop = True

            try:
                rhs = it_that.next()
            except StopIteration:
                rhs_stop = True

            if lhs_stop:
                return True
            if rhs_stop:
                return False
            if lhs >= rhs:
                return False

        return True

    def check(self):
        if self._maxes is None:
            assert self._lists is None
            return

        assert all(sublist[pos - 1] <= sublist[pos]
                   for sublist in self._lists
                   for pos in xrange(1, len(sublist)))

        for pos in xrange(1, len(self._lists)):
            assert self._lists[pos - 1][-1] <= self._lists[pos][0]

        assert len(self._maxes) == len(self._lists)
        assert all(self._maxes[pos] == self._lists[pos][-1]
                   for pos in xrange(len(self._maxes)))
