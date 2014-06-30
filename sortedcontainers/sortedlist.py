# -*- coding: utf-8 -*-
#
# Sorted list implementation.

from __future__ import print_function
from sys import version_info

from bisect import bisect_left, bisect_right, insort
from itertools import chain
from collections import MutableSequence
from operator import iadd

if version_info[0] == 2:
    from itertools import izip as zip
else:
    from functools import reduce

class SortedList(MutableSequence):
    """
    SortedList provides most of the same methods as a list but keeps the items
    in sorted order.
    """

    def __init__(self, iterable=None, load=100):
        """
        SortedList provides most of the same methods as a list but keeps the
        items in sorted order.

        An optional *iterable* provides an initial series of items to populate
        the SortedList.

        An optional *load* specifies the load-factor of the list. The default
        load factor of '100' works well for lists from tens to tens of millions
        of elements.  Good practice is to use a value that is the cube root of
        the list size.  With billions of elements, the best load factor depends
        on your usage.  It's best to leave the load factor at the default until
        you start benchmarking.
        """
        self.clear()
        self._load, self._twice, self._half = load, load * 2, int(load / 2)

        if iterable is not None:
            self.update(iterable)

    def clear(self):
        """Remove all the elements from the list."""
        self._len, self._maxes, self._lists, self._index = 0, None, [], []

    def add(self, val):
        """Add the element *val* to the list."""
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

            del self._index[pos:]
            self._expand(pos)

        self._len += 1

    def _expand(self, pos):
        if len(self._lists[pos]) > self._twice:
            half = self._lists[pos][self._load:]
            self._lists[pos] = self._lists[pos][:self._load]
            self._maxes[pos] = self._lists[pos][-1]
            self._maxes.insert(pos + 1, half[-1])
            self._lists.insert(pos + 1, half)
            del self._index[pos:]

    def update(self, iterable):
        """Grow the list by appending all elements from the *iterable*."""
        values = sorted(iterable)

        if self._maxes is None and len(values) > 0:
            self._lists = [values[pos:(pos + self._load)]
                          for pos in range(0, len(values), self._load)]
            self._maxes = [sublist[-1] for sublist in self._lists]
            self._len = len(values)
            del self._index[:]
        else:
            for val in values:
                self.add(val)

    def __contains__(self, val):
        """Return True if and only if *val* is an element in the list."""
        if self._maxes is None:
            return False

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return False

        idx = bisect_left(self._lists[pos], val)

        return self._lists[pos][idx] == val

    def discard(self, val):
        """
        Remove the first occurrence of *val*.

        If *val* is not a member, does nothing.
        """
        if self._maxes is None:
            return

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return

        idx = bisect_left(self._lists[pos], val)

        if self._lists[pos][idx] == val:
            self._delete(pos, idx)

    def remove(self, val):
        """
        Remove first occurrence of *val*.

        Raises ValueError if *val* is not present.
        """
        if self._maxes is None:
            raise ValueError

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            raise ValueError

        idx = bisect_left(self._lists[pos], val)

        if self._lists[pos][idx] == val:
            self._delete(pos, idx)
        else:
            raise ValueError

    def _delete(self, pos, idx):
        """Delete the item at the given (pos, idx).
        Combines lists that are less than half the load level."""
        del self._lists[pos][idx]
        self._len -= 1
        del self._index[pos:]

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
                prev = pos - 1
                self._lists[prev].extend(self._lists[pos])
                self._maxes[prev] = self._lists[prev][-1]
                del self._maxes[pos]
                del self._lists[pos]
                del self._index[prev:]
                self._expand(prev)

    def _loc(self, pos, idx):
        if pos == 0:
            return idx

        end = len(self._index)

        if pos >= end:

            repeat = pos - end + 1
            prev = self._index[-1] if end > 0 else 0

            for rpt in range(repeat):
                next = prev + len(self._lists[end + rpt])
                self._index.append(next)
                prev = next

        return self._index[pos - 1] + idx

    def _pos(self, idx):
        if self._maxes is None:
            raise IndexError

        if idx < 0:
            last_len = len(self._lists[-1])
            if -idx <= last_len:
                return (len(self._lists) - 1, last_len + idx)
            idx += self._len
        if idx < 0:
            raise IndexError
        if idx >= self._len:
            raise IndexError

        pos = bisect_right(self._index, idx)

        if pos == len(self._index):
            prev = self._index[-1] if pos > 0 else 0

            while prev <= idx:
                next = prev + len(self._lists[pos])
                self._index.append(next)
                prev = next
                pos += 1

            pos -= 1

        if pos == 0:
            return (pos, idx)
        else:
            return (pos, (idx - self._index[pos - 1]))

    def _slice_indices(self, slc):
        start, stop, step = slc.start, slc.stop, slc.step

        if step == 0:
            raise ValueError('slice step cannot be zero')

        # Set defaults for missing values.

        if step is None:
            step = 1

        if step > 0:
            if start is None:
                start = 0

            if stop is None:
                stop = len(self)
            elif stop < 0:
                stop += len(self)
        else:
            if start is None:
                start = len(self) - 1

            if stop is None:
                stop = -1
            elif stop < 0:
                stop += len(self)

        if start < 0:
            start += len(self)

        # Fix indices that are too big or too small.
        # Slice notation is surprisingly permissive
        # where normal indexing would raise IndexError.

        if step > 0:
            if start < 0:
                start = 0
            elif start > len(self):
                start = len(self)

            if stop < 0:
                stop = 0
            elif stop > len(self):
                stop = len(self)
        else:
            if start < 0:
                start = -1
            elif start >= len(self):
                start = len(self) - 1

            if stop < 0:
                stop = -1
            elif stop > len(self):
                stop = len(self)

        # Build iterator for indices.

        if step < 0:
            indices = range(start, stop, step)
        else:
            indices = range(start, stop, step)

        return start, stop, step, indices

    def __delitem__(self, idx):
        """Remove the element located at index *idx* from the list."""
        if isinstance(idx, slice):
            start, stop, step, indices = self._slice_indices(idx)

            # Delete items from greatest index to least so
            # that the indices remain valid throughout iteration.

            if step > 0:
                indices = reversed(indices)

            for index in indices:
                pos, idx = self._pos(index)
                self._delete(pos, idx)
        else:
            pos, idx = self._pos(idx)
            self._delete(pos, idx)

    def __getitem__(self, idx):
        """Return the element at position *idx*."""
        if isinstance(idx, slice):
            start, stop, step, indices = self._slice_indices(idx)

            # Return a list because a negative step could
            # reverse the order of the items and this could
            # be the desired behavior.

            return list(self[index] for index in indices)
        else:
            pos, idx = self._pos(idx)
            return self._lists[pos][idx]

    def _check_order(self, idx, val):
        pos, loc = self._pos(idx)

        if idx < 0: idx += self._len

        # Check that the inserted value is not less than the
        # previous value.

        if idx > 0:
            idx_prev = loc - 1
            pos_prev = pos

            if idx_prev < 0:
                pos_prev -= 1
                idx_prev = len(self._lists[pos_prev]) - 1

            if self._lists[pos_prev][idx_prev] > val:
                raise ValueError

        # Check that the inserted value is not greater than
        # the previous value.

        if idx < (self._len - 1):
            idx_next = loc + 1
            pos_next = pos

            if idx_next == len(self._lists[pos_next]):
                pos_next += 1
                idx_next = 0

            if self._lists[pos_next][idx_next] < val:
                raise ValueError

    def __setitem__(self, index, value):
        """Replace the item at position *index* with *value*."""
        if isinstance(index, slice):
            start, stop, step, indices = self._slice_indices(index)

            if step != 1:
                if not hasattr(value, '__len__'):
                    value = list(value)

                indices = list(indices)

                if len(value) != len(indices):
                    raise ValueError(
                        'attempt to assign sequence of size {0}'
                        ' to extended slice of size {1}'
                        .format(len(value), len(indices)))

                # Keep a log of values that are set so that we can
                # roll back changes if ordering is violated.

                log = []

                for idx, val in zip(indices, value):
                    pos, loc = self._pos(idx)
                    log.append((idx, self._lists[pos][loc], val))
                    self._lists[pos][loc] = val

                try:
                    # Validate ordering of new values.

                    for idx, oldval, newval in log:
                        self._check_order(idx, newval)

                except ValueError:

                    # Roll back changes from log.

                    for idx, oldval, newval in log:
                        pos, loc = self._pos(idx)
                        self._lists[pos][loc] = oldval

                    raise
            else:
                # Test ordering using indexing. If the value given
                # doesn't support getitem, convert it to a list.

                if not hasattr(value, '__getitem__'):
                    value = list(value)

                # Check that the given values are ordered properly.

                ordered = all(value[pos - 1] <= value[pos]
                              for pos in range(1, len(value)))

                if not ordered:
                    raise ValueError

                # Check ordering in context of sorted list.

                if start == 0 or len(value) == 0:
                    # Nothing to check on the lhs.
                    pass
                else:
                    if self[start - 1] > value[0]:
                        raise ValueError

                if stop == len(self) or len(value) == 0:
                    # Nothing to check on the rhs.
                    pass
                else:
                    # "stop" is exclusive so we don't need
                    # to add one for the index.
                    if self[stop] < value[-1]:
                        raise ValueError

                # Delete the existing values.

                del self[index]

                # Insert the new values.

                for idx, val in enumerate(value):
                    self.insert(start + idx, val)
        else:
            pos, loc = self._pos(index)
            self._check_order(index, value)
            self._lists[pos][loc] = value

    def __iter__(self):
        """Create an iterator over the list."""
        return chain.from_iterable(self._lists)

    def __reversed__(self):
        """Create an iterator to traverse the list in reverse."""
        start = len(self._lists) - 1
        iterable = (reversed(self._lists[pos])
                    for pos in range(start, -1, -1))
        return chain.from_iterable(iterable)

    def __len__(self):
        """Return the number of elements in the list."""
        return self._len

    def bisect_left(self, val):
        """
        Similar to the *bisect* module in the standard library, this returns an
        appropriate index to insert *val*. If *val* is already present, the
        insertion point will be before (to the left of) any existing entries.
        """
        if self._maxes is None:
            return 0

        pos = bisect_left(self._maxes, val)

        if pos == len(self._maxes):
            return self._len

        idx = bisect_left(self._lists[pos], val)

        return self._loc(pos, idx)

    def bisect(self, val):
        """Same as bisect_left."""
        return self.bisect_left(val)

    def bisect_right(self, val):
        """
        Same as *bisect_left*, but if *val* is already present, the insertion
        point will be after (to the right of) any existing entries.
        """
        if self._maxes is None:
            return 0

        pos = bisect_right(self._maxes, val)

        if pos == len(self._maxes):
            return self._len

        idx = bisect_right(self._lists[pos], val)

        return self._loc(pos, idx)

    def count(self, val):
        """Return the number of occurrences of *val* in the list."""
        if self._maxes is None:
            return 0

        left = self.bisect_left(val)
        right = self.bisect_right(val)

        return right - left

    def append(self, val):
        """
        Append the element *value* to the list. Raises a ValueError if the *val*
        would violate the sort order.
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
        del self._index[pos:]

        self._expand(pos)

    def extend(self, values):
        """
        Extend the list by appending all elements from the *values*. Raises a
        ValueError if the sort order would be violated.
        """
        if not isinstance(values, list):
            values = list(values)

        if any(values[pos - 1] > values[pos]
               for pos in range(1, len(values))):
            raise ValueError

        offset = 0
        count = len(self._lists) - 1

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

        for idx in range(offset, len(values), self._load):
            self._lists.append(values[idx:(idx + self._load)])
            self._maxes.append(self._lists[-1][-1])

        self._len += len(values)
        del self._index[count:]

    def insert(self, idx, val):
        """
        Insert the element *val* into the list at *idx*. Raises a ValueError if
        the *val* at *idx* would violate the sort order.
        """
        if idx < 0:
            idx += self._len
        if idx < 0:
            idx = 0
        if idx > self._len:
            idx = self._len

        if self._maxes is None:
            # The idx must be zero by the inequalities above.
            self._maxes = [val]
            self._lists = [[val]]
            self._len = 1
            return

        if idx == 0:
            if val > self._lists[0][0]:
                raise ValueError
            else:
                self._lists[0].insert(0, val)
                self._expand(0)
                self._len += 1
                del self._index[:]
                return

        if idx == self._len:
            pos = len(self._lists) - 1
            if self._lists[pos][-1] > val:
                raise ValueError
            else:
                self._lists[pos].append(val)
                self._maxes[pos] = self._lists[pos][-1]
                self._expand(pos)
                self._len += 1
                del self._index[pos:]
                return

        pos, idx = self._pos(idx)
        idx_before = idx - 1
        if idx_before < 0:
            pos_before = pos - 1
            idx_before = len(self._lists[pos_before]) - 1
        else:
            pos_before = pos

        before = self._lists[pos_before][idx_before]
        if before <= val <= self._lists[pos][idx]:
            self._lists[pos].insert(idx, val)
            self._expand(pos)
            self._len += 1
            del self._index[pos:]
        else:
            raise ValueError

    def pop(self, idx=-1):
        """
        Remove and return item at *idx* (default last).  Raises IndexError if
        list is empty or index is out of range.  Negative indexes are supported,
        as for slice indices.
        """
        if (idx < 0 and -idx > self._len) or (idx >= self._len):
            raise IndexError

        pos, idx = self._pos(idx)
        val = self._lists[pos][idx]
        self._delete(pos, idx)

        return val

    def index(self, val, start=None, stop=None):
        """
        Return the smallest *k* such that L[k] == val and i <= k < j`.  Raises
        ValueError if *val* is not present.  *stop* defaults to the end of the
        list. *start* defaults to the beginning. Negative indexes are supported,
        as for slice indices.
        """
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
        """Very efficiently convert the SortedList to a list."""
        return reduce(iadd, self._lists, [])

    def __add__(self, that):
        """
        Return a new sorted list extended by appending all elements from
        *that*. Raises a ValueError if the sort order would be violated.
        """
        values = self.as_list()
        values.extend(that)
        return SortedList(values)

    def __iadd__(self, that):
        """
        Increase the length of the list by appending all elements from
        *that*. Raises a ValueError if the sort order would be violated.
        """
        self.update(that)
        return self

    def __mul__(self, that):
        """
        Return a new sorted list containing *that* shallow copies of each item
        in SortedList.
        """
        values = self.as_list() * that
        return SortedList(values)

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
        return ((self._len == len(that))
                and all(lhs == rhs for lhs, rhs in zip(self, that)))

    def __ne__(self, that):
        """Compare two iterables for inequality."""
        return ((self._len != len(that))
                or any(lhs != rhs for lhs, rhs in zip(self, that)))

    def __lt__(self, that):
        """Compare two iterables for less than."""
        return ((self._len <= len(that))
                and all(lhs < rhs for lhs, rhs in zip(self, that)))

    def __le__(self, that):
        """Compare two iterables for less than equal."""
        return ((self._len <= len(that))
                and all(lhs <= rhs for lhs, rhs in zip(self, that)))

    def __gt__(self, that):
        """Compare two iterables for greater than."""
        return ((self._len >= len(that))
                and all(lhs > rhs for lhs, rhs in zip(self, that)))

    def __ge__(self, that):
        """Compare two iterables for greater than equal."""
        return ((self._len >= len(that))
                and all(lhs >= rhs for lhs, rhs in zip(self, that)))

    def __repr__(self):
        """Return string representation of SortedList."""
        return 'SortedList({0})'.format(repr(self.as_list()))

    def _check(self):
        try:
            # Check load parameters.

            assert self._load >= 4
            assert self._half == int(self._load / 2)
            assert self._twice == (self._load * 2)

            # Check empty sorted list case.

            if self._maxes is None:
                assert self._lists == []
                return

            assert len(self._maxes) > 0 and len(self._lists) > 0

            # Check all sublists are sorted.

            assert all(sublist[pos - 1] <= sublist[pos]
                       for sublist in self._lists
                       for pos in range(1, len(sublist)))

            # Check beginning/end of sublists are sorted.

            for pos in range(1, len(self._lists)):
                assert self._lists[pos - 1][-1] <= self._lists[pos][0]

            # Check length of _maxes and _lists match.

            assert len(self._maxes) == len(self._lists)

            # Check _maxes is a map of _lists.

            assert all(self._maxes[pos] == self._lists[pos][-1]
                       for pos in range(len(self._maxes)))

            # Check load level is less than _twice.

            assert all(len(sublist) <= self._twice for sublist in self._lists)

            # Check load level is greater than _half for all
            # but the last sublist.

            assert all(len(self._lists[pos]) >= self._half
                       for pos in range(0, len(self._lists) - 1))

            # Check length.

            assert self._len == sum(len(sublist) for sublist in self._lists)

            # Check cumulative sum cache.

            cumulative_sum_len = [len(self._lists[0])]
            for pos in range(1, len(self._index)):
                cumulative_sum_len.append(cumulative_sum_len[-1] + len(self._lists[pos]))
            assert all((self._index[pos] == cumulative_sum_len[pos])
                       for pos in range(len(self._index)))

        except AssertionError:
            import sys, traceback

            traceback.print_exc(file=sys.stdout)

            print(self._len, self._load, self._half, self._twice)
            print(self._index)
            print(self._maxes)
            print(self._lists)

            raise
