SortedSet
=========

.. class:: SortedSet(iterable=None, load=100, _set=None):

   A :class:`SortedSet` provides the same methods as a :class:`set`.
   Additionally, a :class:`SortedSet:` maintains its items in sorted
   order, allowing the :class:`SortedSet` to be indexed.

   An optional *iterable* provides an initial series of items to
   populate the :class:`SortedSet`.

   Unlike a :class:`set`, a :class:`SortedSet` does not require items
   to be hashable. But it does require that items be comparable.

   .. method:: x in S

      Returns True if and only if *x* is an element in the set.

      :rtype: :class:`bool`

   .. _SortedSet.delitem:
   .. method:: del S[i]

      Removes the element located at index *i* from the set.

   .. method:: del S[i:j]

      Removes the elements from *i* to *j* from the set.

   .. method:: S < S2

      Test whether the set is a proper subset of *S2*, that is, ``S <= S2
      and S != other``.

      :rtype: :class:`bool`

   .. method:: S > S2

      Test whether the set is a proper superset of *S2*, that is, ``S
      >= S2 and S != S2``.

      :rtype: :class:`bool`

   .. method:: S[i]

      Returns the element at position *i*.

      :rtype: item

   .. method:: S[i:j]

      Returns a new SortedSet containing the elements from *i* to *j*.

      :rtype: :class:`SortedSet`

   .. method:: S *= k

      Increase the length of the set by a factor of *k*, by inserting
      *k-1* additional shallow copies of each item in the set.

   .. method:: iter(S)

      Creates an iterator over the set.

      :rtype: iterator

   .. method:: len(S)

      Returns the number of elements in the set.

      :rtype: :class:`int`

   .. method:: S * k or k * S

      Returns a new sorted set containing *k* shallow copies of each
      item in S.

      :rtype: :class:`SortedSet`

   .. method:: reversed(S)

      Creates an iterator to traverse the set in reverse.

      :rtype: iterator

   .. _SortedSet.add:
   .. method:: S.add(value)

      Add the element *value* to the set.

   .. _sortedlist.bisect_left:
   .. method:: L.bisect_left(value)

      Similarly to the ``bisect`` module in the standard library, this
      returns an appropriate index to insert *value* in *L*. If *value* is
      already present in *L*, the insertion point will be before (to the
      left of) any existing entries.

   .. method:: L.bisect(value)

      Same as :ref:`bisect_left <sortedlist.bisect_right>`.

   .. method:: L.bisect_right(value)

      Same thing as :ref:`bisect_left <sortedlist.bisect_left>`, but if
      *value* is already present in *L*, the insertion point will be after
      (to the right of) any existing entries.

   .. method:: S.clear()

      Remove all elements from the set.

   .. method:: S.copy()

      Creates a shallow copy of the set.

      :rtype: :class:`SortedSet`

   .. method:: S.count(value)

      Returns the number of occurrences of *value* in the set.

      :rtype: :class:`int`

   .. method:: S.difference(S2, ...)
               S - S2 - ...

      Return a new set with elements in the set that are not in the others.

      :rtype: :class:`SortedSet`

   .. method:: S.difference_update(S2, ...)
               S -= S2 | ...

      Update the set, removing elements found in keeping only elements
      found in any of the others.

   .. _SortedSet.discard:
   .. method:: S.discard(value)

      Removes the first occurrence of *value*.  If *value* is not a
      member, does nothing.

   .. method:: S.index(value, [start, [stop]])

      Returns the smallest *k* such that :math:`S[k] == x` and
      :math:`i <= k < j`.  Raises ValueError if *value* is not
      present.  *stop* defaults to the end of the set.  *start*
      defaults to the beginning.  Negative indexes are supported, as
      for slice indices.

      :rtype: :class:`int`

   .. method:: S.intersection(S2, ...)
               S & S2 & ...

      Return a new set with elements common to the set and all others.

      :rtype: :class:`SortedSet`

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

   .. method:: S.symmetric_difference(S2)
               S ^ S2

      Return a new set with element in either set but not both.

      :rtype: :class:`SortedSet`

   .. method:: S.symmetric_difference_update(S2)
               S ^= S2

      Update the set, keeping only elements found in either set, but
      not in both.

   .. method:: S.pop([index])

      Removes and return item at index (default last).  Raises
      IndexError if set is empty or index is out of range.  Negative
      indexes are supported, as for slice indices.

      :rtype: item

   .. _SortedSet.remove:
   .. method:: S.remove(value)

      Remove first occurrence of *value*.  Raises ValueError if
      *value* is not present.

   .. method:: S.union(S2, ...)
               S | S2 | ...

      Return a new SortedSet with elements from the set and all
      others.  The new SortedSet will be sorted according to the key
      of the leftmost set.

      :rtype: :class:`SortedSet`

   .. method:: S.update(S2, ...)
               S |= S2 | ...

      Update the set, adding elements from all others.
