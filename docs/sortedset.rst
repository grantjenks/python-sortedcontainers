SortedSet
=========

:doc:`SortedContainers<index>` is an Apache2 licensed Python sorted collections
library, written in pure-Python, and fast as C-extensions. SortedSet API
documentation is detailed below. The :doc:`introduction<introduction>` is the
best way to get started.

.. currentmodule:: sortedcontainers

.. class:: SortedSet(iterable=None, load=1000, _set=None):

   A :class:`SortedSet` provides the same methods as a :class:`set`.
   Additionally, a :class:`SortedSet` maintains its items in sorted
   order, allowing the :class:`SortedSet` to be indexed.

   An optional *iterable* provides an initial series of items to
   populate the :class:`SortedSet`.

   An optional *key* argument defines a callable that, like the `key` argument
   to Python's `sorted` function, extracts a comparison key from each set
   item. If no function is specified, the default compares the set items
   directly.

   An optional *load* specifies the load-factor of the set. The default load
   factor of '1000' works well for sets from tens to tens of millions of
   elements.  Good practice is to use a value that is the square or cube root of
   the set size.  With billions of elements, the best load factor depends on
   your usage.  It's best to leave the load factor at the default until you
   start benchmarking. See :doc:`implementation details <implementation>` for
   more information.

   Unlike a :class:`set`, a :class:`SortedSet` requires items be hashable and
   comparable. :class:`SortedSet` implements the MutableSet and Sequence
   Abstract Base Class types.

   .. _SortedSet.__contains__:
   .. method:: x in S

      Return True if and only if *x* is an element in the set.

      :rtype: :class:`bool`

   .. _SortedSet.__delitem__:
   .. method:: del S[i]

      Remove the element located at index *i* from the set.

   .. method:: del S[i:j]

      Remove the elements from *i* to *j* from the set.

   .. method:: S < S2

      Test whether the set is a proper subset of *S2*, that is, ``S <= S2
      and S != other``.

      :rtype: :class:`bool`

   .. method:: S > S2

      Test whether the set is a proper superset of *S2*, that is, ``S
      >= S2 and S != S2``.

      :rtype: :class:`bool`

   .. _SortedSet.__getitem__:
   .. method:: S[i]

      Return the element at position *i*.

      :rtype: item

   .. _SortedSet.__setitem__:
   .. method:: S[i] = v

      Remove the element located at index *i* from the set and insert element
      *v*. Supports slice notation. Raises a :exc:`ValueError` if the sort order
      would be violated.

   .. method:: S[i:j]

      Return a new SortedSet containing the elements from *i* to *j*.

      :rtype: :class:`SortedSet`

   .. _SortedSet.__iter__:
   .. method:: iter(S)

      Return an iterator over the Set. Elements are iterated in their sorted
      order.

      Iterating the Set while adding or deleting values may raise a
      `RuntimeError` or fail to iterate over all entries.

      :rtype: iterator

   .. method:: len(S)

      Return the number of elements in the set.

      :rtype: :class:`int`

   .. method:: reversed(S)

      Return an iterator over the Set. Elements are iterated in their reverse
      sorted order.

      Iterating the Set while adding or deleting values may raise a
      `RuntimeError` or fail to iterate over all entries.

      :rtype: iterator

   .. _SortedSet.add:
   .. method:: S.add(value)

      Add the element *value* to the set.

   .. _sortedlist.bisect_left:
   .. method:: L.bisect_left(value)

      Similar to the ``bisect`` module in the standard library, this
      returns an appropriate index to insert *value* in *L*. If *value* is
      already present in *L*, the insertion point will be before (to the
      left of) any existing entries.

      :rtype: :class:`int`

   .. method:: L.bisect(value)

      Same as :ref:`bisect_right <sortedlist.bisect_right>`.

      :rtype: :class:`int`

   .. method:: L.bisect_right(value)

      Same as :ref:`bisect_left <sortedlist.bisect_left>`, but if
      *value* is already present in *L*, the insertion point will be after
      (to the right of) any existing entries.

      :rtype: :class:`int`

   .. _SortedSet.bisect_key_left:
   .. method:: d.bisect_key_left(key)

      Similar to the ``bisect`` module in the standard library, this returns an
      appropriate index to insert a value with a given *key*. If values with
      *key* are already present, the insertion point will be before (to the
      left of) any existing entries. This method is present only if the sorted
      set was constructed with a key function.

      :rtype: :class:`int`

   .. method:: d.bisect_key(key)

      Same as :ref:`bisect_key_right <SortedSet.bisect_key_right>`.

      :rtype: :class:`int`

   .. _SortedSet.bisect_key_right:
   .. method:: d.bisect_key_right(key)

      Same as :ref:`bisect_key_left <SortedSet.bisect_key_left>`, but
      if *key* is already present, the insertion point will be after (to the
      right of) any existing entries.

      :rtype: :class:`int`

   .. method:: S.clear()

      Remove all elements from the set.

   .. method:: S.copy()

      Create a shallow copy of the set.

      :rtype: :class:`SortedSet`

   .. method:: S.count(value)

      Return the number of occurrences of *value* in the set.

      :rtype: :class:`int`

   .. _SortedSet.difference:
   .. method:: S.difference(S2, ...)
               S - S2 - ...

      Return a new set with elements in the set that are not in the others.

      :rtype: :class:`SortedSet`

   .. _SortedSet.difference_update:
   .. method:: S.difference_update(S2, ...)
               S -= S2 | ...

      Update the set, removing elements found in keeping only elements
      found in any of the others.

   .. _SortedSet.discard:
   .. method:: S.discard(value)

      Remove the first occurrence of *value*.  If *value* is not a
      member, does nothing.

   .. method:: S.index(value, [start, [stop]])

      Return the smallest *k* such that :math:`S[k] == x` and
      :math:`i <= k < j`.  Raises ValueError if *value* is not
      present.  *stop* defaults to the end of the set.  *start*
      defaults to the beginning.  Negative indexes are supported, as
      for slice indices.

      :rtype: :class:`int`

   .. _SortedSet.intersection:
   .. method:: S.intersection(S2, ...)
               S & S2 & ...

      Return a new set with elements common to the set and all others.

      :rtype: :class:`SortedSet`

   .. _SortedSet.intersection_update:
   .. method:: S.intersection_update(S2, ...)
               S &= S2 & ...

      Update the set, keeping only elements found in it and all
      others.

   .. method:: S.isdisjoint(S2)

      Return True if the set has no elements in common with *S2*.
      Sets are disjoint if and only if their intersection is the empty
      set.

      :rtype: :class:`bool`

   .. method:: S.issubset(S2)
               S <= S2

      Test whether every element in the set is in *S2*

      :rtype: :class:`bool`

   .. method:: S.issuperset(S2)
              S >= S2

      Test whether every element in *S2* is in the set.

      :rtype: :class:`bool`

   .. _SortedSet.symmetric_difference:
   .. method:: S.symmetric_difference(S2)
               S ^ S2

      Return a new set with elements in either set but not both.

      :rtype: :class:`SortedSet`

   .. _SortedSet.symmetric_difference_update:
   .. method:: S.symmetric_difference_update(S2)
               S ^= S2

      Update the set, keeping only elements found in either set, but
      not in both.

   .. _SortedSet.pop:
   .. method:: S.pop([index])

      Remove and return item at index (default last).  Raises
      IndexError if set is empty or index is out of range.  Negative
      indexes are supported, as for slice indices.

      :rtype: item

   .. _SortedSet.remove:
   .. method:: S.remove(value)

      Remove first occurrence of *value*.  Raises ValueError if
      *value* is not present.

   .. _SortedSet.union:
   .. method:: S.union(S2, ...)
               S | S2 | ...

      Return a new SortedSet with elements from the set and all
      others.

      :rtype: :class:`SortedSet`

   .. _SortedSet.update:
   .. method:: S.update(S2, ...)
               S |= S2 | ...

      Update the set, adding elements from all others.

   .. method:: S.islice(start=None, stop=None, reverse=False)

      Returns an iterator that slices `self` from `start` to `stop` index,
      inclusive and exclusive respectively.

      When `reverse` is `True`, values are yielded from the iterator in
      reverse order.

      Both `start` and `stop` default to `None` which is automatically
      inclusive of the beginning and end.

      :rtype: iterator

   .. method:: S.irange(minimum=None, maximum=None, inclusive=(True, True), reverse=False)

      Create an iterator of values between `minimum` and `maximum`.

      `inclusive` is a pair of booleans that indicates whether the minimum
      and maximum ought to be included in the range, respectively. The
      default is (True, True) such that the range is inclusive of both
      minimum and maximum.

      Both `minimum` and `maximum` default to `None` which is automatically
      inclusive of the start and end of the list, respectively.

      When `reverse` is `True` the values are yielded from the iterator in
      reverse order; `reverse` defaults to `False`.

      When initialized with a key-function, an `irange_key` method is also
      provided with :ref:`similar semantics<SortedListWithKey.irange_key>`.

      :rtype: iterator
