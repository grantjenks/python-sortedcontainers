SortedList
==========

.. class:: SortedList(iterable=None, load=1000)

   A :class:`SortedList` provides most of the same methods as a :class:`list`,
   but keeps the items in sorted order.  To add an element to the SortedList,
   use :ref:`add <SortedList.add>`.  To add several elements, use :ref:`update
   <SortedList.update>`.  To remove an element, use :ref:`discard
   <SortedList.discard>`, :ref:`remove <SortedList.remove>`, or :ref:`del L[i]
   <SortedList.__delitem__>`.

   An optional *iterable* provides an initial series of items to
   populate the :class:`SortedList`.

   An optional *load* specifies the load-factor of the list. The default load
   factor of '1000' works well for lists from tens to tens of millions of
   elements.  Good practice is to use a value that is the cube root of the list
   size.  With billions of elements, the best load factor depends on your usage.
   It's best to leave the load factor at the default until you start
   benchmarking. See :doc:`implementation details <implementation>` for more
   information.

   :class:`SortedList` implements the MutableSequence Abstract Base Class type.

   .. _SortedList.__contains__:
   .. method:: x in L

      Return True if and only if *x* is an element in the list.

      :rtype: :class:`bool`

   .. _SortedList.__delitem__:
   .. method:: del L[i]

      Remove the element located at index *i* from the list.

   .. method:: del L[i:j]

      Remove the elements from *i* to *j* from the list. Also note that *step*
      is supported in slice syntax.

   .. _SortedList.__eq__:
   .. method:: L == L2, L != L2, L < L2, L <= L2, L > L2, L >= L2

      Compare two lists.  For full details see `Comparisons
      <http://docs.python.org/reference/expressions.html>`_ in
      the Python language reference.

      :rtype: :class:`bool`

   .. _SortedList.__getitem__:
   .. method:: L[i]

      Return the element at position *i*.

      :rtype: item

   .. method:: L[i:j]

      Return a new :class:`list` containing the elements from *i* to *j*. Also
      note that *step* is supported in slice syntax.

      :rtype: :class:`list`

   .. method:: L *= k

      Increase the length of the list by a factor of *k*, by inserting
      *k-1* additional shallow copies of each item in the list.

   .. _SortedList.__iter__:
   .. method:: iter(L)

      Create an iterator over the list.

      :rtype: iterator

   .. method:: len(L)

      Return the number of elements in the list.

      :rtype: :class:`int`

   .. _SortedList.__mul__:
   .. method:: L * k or k * L

      Return a new sorted list containing *k* shallow copies of each
      item in L.

      :rtype: :class:`SortedList`

   .. _SortedList.__add__:
   .. method:: L + k

      Return a new sorted list extended by appending all elements from
      *k*. Raises a :exc:`ValueError` if the sort order would be violated.

      :rtype: :class:`SortedList`

   .. _SortedList.__iadd__:
   .. method:: L += k

      Increase the length of the list by appending all elements from *k*. Raises
      a :exc:`ValueError` if the sort order would be violated.

   .. method:: reversed(L)

      Create an iterator to traverse the list in reverse.

      :rtype: iterator

   .. _SortedList.__setitem__:
   .. method:: L[i] = x

      Replace the item at position *i* of *L* with *x*. Supports slice
      notation. Raises a :exc:`ValueError` if the sort order would be violated.

   .. method:: L[i:j] = iterable

      Replace the items at positions *i* through *j* with the contents of
      *iterable*. Also note that *step* is supported in slice syntax.

   .. _SortedList.add:
   .. method:: L.add(value)

      Add the element *value* to the list.

   .. _SortedList.bisect_left:
   .. method:: L.bisect_left(value)

      Similar to the ``bisect`` module in the standard library, this
      returns an appropriate index to insert *value* in *L*. If *value* is
      already present in *L*, the insertion point will be before (to the
      left of) any existing entries.

   .. _SortedList.bisect:
   .. method:: L.bisect(value)

      Same as :ref:`bisect_left <SortedList.bisect_right>`.

   .. _SortedList.bisect_right:
   .. method:: L.bisect_right(value)

      Same as :ref:`bisect_left <SortedList.bisect_left>`, but if
      *value* is already present in *L*, the insertion point will be after
      (to the right of) any existing entries.

   .. _SortedList.count:
   .. method:: L.count(value)

      Return the number of occurrences of *value* in the list.

      :rtype: :class:`int`

   .. _SortedList.discard:
   .. method:: L.discard(value)

      Remove the first occurrence of *value*.  If *value* is not a
      member, does nothing.

   .. _SortedList.index:
   .. method:: L.index(value, [start, [stop]])

      Return the smallest *k* such that :math:`L[k] == x` and
      :math:`i <= k < j`.  Raises ValueError if *value* is not
      present.  *stop* defaults to the end of the list.  *start*
      defaults to the beginning.  Negative indexes are supported, as
      for slice indices.

      :rtype: :class:`int`

   .. _SortedList.pop:
   .. method:: L.pop([index])

      Remove and return item at index (default last).  Raises :exc:`IndexError`
      if list is empty or index is out of range.  Negative indexes are
      supported, as for slice indices.

      :rtype: item

   .. _SortedList.remove:
   .. method:: L.remove(value)

      Remove first occurrence of *value*.  Raises :exc:`ValueError` if
      *value* is not present.

   .. _SortedList.update:
   .. method:: L.update(iterable)

      Grow the list by inserting all elements from the *iterable*.

   .. method:: L.clear()

      Remove all the elements from the list.

   .. _SortedList.append:
   .. method:: L.append(value)

      Append the element *value* to the list. Raises a :exc:`ValueError` if the
      *value* would violate the sort order.

   .. _SortedList.extend:
   .. method:: L.extend(iterable)

      Extend the list by appending all elements from the *iterable*. Raises a
      :exc:`ValueError` if the sort order would be violated.

   .. _SortedList.insert:
   .. method:: L.insert(index, value)

      Insert the element *value* into the list at *index*. Raises a
      :exc:`ValueError` if the *value* at *index* would violate the sort order.

   .. method:: L.as_list()

      Very efficiently convert the :class:`SortedList` to a class:`list`.

      :rtype: :class:`list`
