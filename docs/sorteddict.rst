SortedDict
==========

:doc:`SortedContainers<index>` is an Apache2 licensed Python sorted collections
library, written in pure-Python, and fast as C-extensions. SortedDict API
documentation is detailed below. The :doc:`introduction<introduction>` is the
best way to get started.

.. currentmodule:: sortedcontainers

.. class:: SortedDict(*args, **kwargs)

   A :class:`SortedDict` provides the same methods as a :class:`dict`.
   Additionally, a :class:`SortedDict` efficiently maintains its keys in sorted
   order.  Consequently, the :ref:`keys <SortedDict.keys>` method will return
   the keys in sorted order, the :ref:`popitem <SortedDict.popitem>` method will
   remove the item with the highest key, etc.

   An optional *key* argument defines a callable that, like the `key` argument
   to Python's `sorted` function, extracts a comparison key from each dict
   key. If no function is specified, the default compares the dict keys
   directly. The `key` argument must be provided as a positional argument and
   must come before all other arguments.

   An optional *load* argument defines the load factor of the internal list used
   to maintain sort order. If present, this argument must come before an
   iterable. The default load factor of '1000' works well for lists from tens to
   tens of millions of elements.  Good practice is to use a value that is the
   square or cube root of the list size.  With billions of elements, the best
   load factor depends on your usage.  It's best to leave the load factor at the
   default until you start benchmarking. See :doc:`implementation details
   <implementation>` for more information.

   An optional *iterable* provides an initial series of items to populate the
   :class:`SortedDict`.  Each item in the series must itself contain two items.
   The first is used as a key in the new dictionary, and the second as the key's
   value. If a given key is seen more than once, the last value associated with
   it is retained in the new dictionary.

   If keyword arguments are given, the keywords themselves with their associated
   values are added as items to the dictionary. If a key is specified both in
   the positional argument and as a keyword argument, the value associated with
   the keyword is retained in the dictionary. For example, these all return a
   dictionary equal to ``{"one": 2, "two": 3}``:

   * ``SortedDict(one=2, two=3)``
   * ``SortedDict({'one': 2, 'two': 3})``
   * ``SortedDict(zip(('one', 'two'), (2, 3)))``
   * ``SortedDict([['two', 3], ['one', 2]])``

   The first example only works for keys that are valid Python identifiers; the
   others work with any valid keys.

   :class:`SortedDict` inherits from the built-in `dict` type.

   .. _SortedDict.__contains__:
   .. method:: x in d

      Return True if and only if *x* is a key in the dictionary.

      :rtype: :class:`bool`

   .. _SortedDict.__delitem__:
   .. method:: del d[key]

      Remove ``d[key]`` from *d*.  Raises a :exc:`KeyError` if *key*
      is not in the dictionary.

   .. _SortedDict.__getitem__:
   .. method:: d[key]

      Return the item of *d* with key *key*.  Raises a :exc:`KeyError`
      if *key* is not in the dictionary.

      :rtype: value

   .. method:: D == D2, D != D2

      Test two dictionaries for equality (or inequality). Mappings compare
      equal if and only if they have the same length, if all of the keys of *D*
      may be found in *D2*, and all of the corresponding values compare equal.

      :rtype: :class:`bool`

   .. _SortedDict.__iter__:
   .. method:: iter(d)

      Return an iterator over the sorted keys of the dictionary.

      Iterating the Mapping while adding or deleting keys may raise a
      `RuntimeError` or fail to iterate over all entries.

      :rtype: iterator

   .. _SortedDict.__reversed__:
   .. method:: reversed(d)

      Return a reversed iterator over the sorted keys of the dictionary.

      Iterating the Mapping while adding or deleting keys may raise a
      `RuntimeError` or fail to iterate over all entries.

      :rtype: iterator

   .. method:: len(d)

      Return the number of (key, value) pairs in the dictionary.

      :rtype: :class:`int`

   .. _SortedDict.__setitem__:
   .. method:: d[key] = value

      Set `d[key]` to *value*.

   .. method:: d.clear()

      Remove all elements from the sorted dictionary.

   .. method:: d.copy()

      Create a shallow copy of the dictionary.

      :rtype: :class:`SortedDict`

   .. method:: d.fromkeys(seq, value=None)

      Create a new dictionary with keys from *seq* and values set to
      *value*.

      :meth:`fromkeys` is a class method that returns a new
      dictionary.  *value* defaults to ``None``.

      :rtype: :class:`SortedDict`

   .. method:: d.get(key, default=None)

      Return the value for *key* if *key* is in the dictionary, else
      *default*.  If *default* is not given, it defaults to ``None``,
      so that this method never raises a :exc:`KeyError`.

      :rtype: value

   .. method:: d.items()

      In Python 2, returns a list of the dictionary's items (``(key,
      value)`` pairs).

      In Python 3, returns a new :class:`ItemsView` of the dictionary's
      items.  In addition to the methods provided by the built-in `view
      <http://docs.python.org/release/3.1/library/stdtypes.html#dictionary-view-objects>`_,
      the :class:`ItemsView` is indexable (e.g., ``d.items()[5]``).

      :rtype: :class:`list` or :class:`ItemsView`

   .. _SortedDict.keys:
   .. method:: d.keys()

      In Python 2, return a :class:`SortedSet` of the dictionary's keys.

      In Python 3, return a new :class:`KeysView` of the dictionary's
      keys.  In addition to the methods provided by the built-in `view
      <http://docs.python.org/release/3.1/library/stdtypes.html#dictionary-view-objects>`_,
      the :class:`KeysView` is indexable (e.g., ``d.keys()[5]``).

      :rtype: :class:`SortedSet` or :class:`KeysView`

   .. method:: d.pop(key[, default])

      If *key* is in the dictionary, remove it and return its value,
      else return *default*. If *default* is not given and *key* is not in
      the dictionary, a :exc:`KeyError` is raised.

      :rtype: value

   .. _SortedDict.popitem:
   .. method:: d.popitem(last=True)

      Remove and return a ``(key, value)`` pair from the dictionary. If
      ``last=True`` (default) then remove the *greatest* key from the
      dictionary. Else, remove the *least* key from the dictionary.

      If the dictionary is empty, calling :meth:`popitem` raises a
      :exc:`KeyError`.

      :rtype: (key, value) tuple

   .. method:: d.peekitem(index=-1)

      Return ``(key, value)`` item pair at index.

      Unlike :ref:`popitem<SortedDict.popitem>`, the sorted dictionary is not
      modified. Index defaults to -1, the *last/greatest* key in the
      dictionary. Specify ``index=0`` to lookup the *first/least* key in the
      dictionary.

      If index is out of range, raise :exc:`IndexError`.

      :rtype: (key, value) tuple

   .. method:: d.setdefault(key, default=None)

      If *key* is in the dictionary, return its value.  If not,
      insert *key* with a value of *default* and return
      *default*.  *default* defaults to ``None``.

   .. method:: d.update(other, ...)

      Update the dictionary with the key/value pairs from *other*,
      overwriting existing keys.

      :meth:`update` accepts either another dictionary object or an
      iterable of key/value pairs (as a tuple or other iterable of
      length two).  If keyword arguments are specified, the dictionary
      is then updated with those key/value pairs: ``d.update(red=1,
      blue=2)``.

   .. method:: d.values()

      In Python 2, return a list of the dictionary's values.

      In Python 3, return a new :class:`ValuesView` of the dictionary's
      values.  In addition to the methods provided by the built-in `view
      <http://docs.python.org/release/3.1/library/stdtypes.html#dictionary-view-objects>`_,
      the :class:`ValuesView` is indexable (e.g., ``d.values()[5]``).

      :rtype: :class:`list` or :class:`ValuesView`

   .. _SortedDict.index:
   .. method:: d.index(key, [start, [stop]])

      Return the smallest *k* such that :math:`d.iloc[k] == key` and
      :math:`i <= k < j`.  Raises :exc:`ValueError` if *key* is not
      present.  *stop* defaults to the end of the set.  *start*
      defaults to the beginning.  Negative indexes are supported, as
      for slice indices.

      :rtype: :class:`int`

   .. _SortedDict.bisect_left:
   .. method:: d.bisect_left(key)

      Similar to the ``bisect`` module in the standard library, this returns an
      appropriate index to insert *key* in SortedDict. If *key* is already
      present in SortedDict, the insertion point will be before (to the left of)
      any existing entries.

      :rtype: :class:`int`

   .. _SortedDict.bisect:
   .. method:: d.bisect(key)

      Same as :ref:`bisect_right <SortedDict.bisect_right>`.

      :rtype: :class:`int`

   .. _SortedDict.bisect_right:
   .. method:: d.bisect_right(key)

      Same as :ref:`bisect_left <SortedDict.bisect_left>`, but if *key* is
      already present in SortedDict, the insertion index will be after (to the
      right of) any existing entries.

      :rtype: :class:`int`

   .. _SortedDict.bisect_key_left:
   .. method:: d.bisect_key_left(key)

      Similar to the ``bisect`` module in the standard library, this returns an
      appropriate index to insert a value with a given *key*. If values with
      *key* are already present, the insertion point will be before (to the
      left of) any existing entries. This method is present only if the sorted
      dict was constructed with a key function. In this context, *key* refers
      to the result of the key function applied to the dictionary key.

      :rtype: :class:`int`

   .. method:: d.bisect_key(key)

      Same as :ref:`bisect_key_right <SortedDict.bisect_key_right>`.

      :rtype: :class:`int`

   .. _SortedDict.bisect_key_right:
   .. method:: d.bisect_key_right(key)

      Same as :ref:`bisect_key_left <SortedDict.bisect_key_left>`, but
      if *key* is already present, the insertion point will be after (to the
      right of) any existing entries.

      :rtype: :class:`int`

   .. _SortedDict.iloc:
   .. method:: d.iloc[pos]

      Very efficiently return the key at index *pos* in iteration. Supports
      negative indices and slice notation. Raises :exc:`IndexError` on invalid
      *pos*.

      :rtype: key or :class:`list`

   .. method:: del d.iloc[index]

      Remove the ``d[d.iloc[index]]`` from *d*.  Supports negative indices and
      slice notation.  Raises :exc:`IndexError` on invalid *index*.

   .. method:: d.islice(start=None, stop=None, reverse=False)

      Returns an iterator that slices keys from `start` to `stop` index,
      inclusive and exclusive respectively.

      When `reverse` is `True`, values are yielded from the iterator in
      reverse order.

      Both `start` and `stop` default to `None` which is automatically
      inclusive of the beginning and end.

      :rtype: iterator

   .. method:: d.irange(minimum=None, maximum=None, inclusive=(True, True), reverse=False)

      Create an iterator of keys between `minimum` and `maximum`.

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

.. class:: KeysView

   A KeysView object is a dynamic view of the dictionary's keys, which
   means that when the dictionary's keys change, the view reflects
   those changes.

   :class:`KeysView` implements the KeysView, Set, and Sequence Abstract
   Base Class types.

   .. method:: len(keysview)

      Return the number of entries in the dictionary.

      :rtype: :class:`int`

   .. method:: iter(keysview)

      Return an iterator over the keys in the dictionary.  Keys are
      iterated over in their sorted order.

      Iterating views while adding or deleting entries in the dictionary
      may raise a :exc:`RuntimeError` or fail to iterate over all
      entries.

      :rtype: iterator

   .. method:: reversed(keysview)

      Return a reversed iterator over the keys in the dictionary.

      Iterating views while adding or deleting entries in the dictionary
      may raise a :exc:`RuntimeError` or fail to iterate over all
      entries.

      :rtype: iterator

   .. method:: x in keysview

      Return ``True`` iff *x* is one of the underlying dictionary's
      keys.

      :rtype: :class:`bool`

   .. method:: keysview[i]

      Return the key at position *i*.

      :rtype: value

   .. _KeysView.and:
   .. method:: keysview & other

      Return the intersection of the keys and the other object as
      a new set.

      :rtype: :class:`SortedSet`

   .. _KeysView.or:
   .. method:: keysview | other

      Return the union of the keys and the other object as a new set.

      :rtype: :class:`SortedSet`

   .. _KeysView.sub:
   .. describe:: keysview - other

      Return the difference between the keys and the other object (all
      keys that aren't in *other*) as a new set.

      :rtype: :class:`SortedSet`

   .. _KeysView.xor:
   .. describe:: keysview ^ other

      Return the symmetric difference (all elements either in the keys
      or *other*, but not in both) of the keys and the other object as
      a new set.

      :rtype: :class:`SortedSet`

   .. method:: keysview.count(key)

      Return the number of occurrences of *key* in the set.

      :rtype: :class:`int`

   .. method:: keysview.index(key, [start, [stop]])

      Return the smallest *k* such that :math:`keysview[k] == x` and
      :math:`i <= k < j`.  Raises :exc:`KeyError` if *key* is not
      present.  *stop* defaults to the end of the set.  *start*
      defaults to the beginning.  Negative indexes are supported, as
      for slice indices.

      :rtype: :class:`int`

.. class:: ValuesView

   A ValuesView object is a dynamic view of the dictionary's values,
   which means that when the dictionary's values change, the view
   reflects those changes.

   :class:`ValuesView` implements the ValuesView and Sequence Abstract
   Base Class types.

   .. method:: len(valuesview)

      Return the number of entries in the dictionary.

      :rtype: :class:`int`

   .. method:: iter(valuesview)

      Return an iterator over the values in the dictionary.  Values are
      iterated over in sorted order of the keys.

      Iterating views while adding or deleting entries in the dictionary
      may raise a :exc:`RuntimeError` or fail to iterate over all
      entries.

      :rtype: iterator

   .. method:: reversed(valuesview)

      Return a reversed iterator over the values in the dictionary.  Values
      are iterated over in reversed sorted order of the keys.

      Iterating views while adding or deleting entries in the dictionary
      may raise a :exc:`RuntimeError` or fail to iterate over all
      entries.

      :rtype: iterator

   .. method:: x in valuesview

      Return ``True`` iff *x* is one of the underlying dictionary's
      values.

      :rtype: :class:`bool`

   .. method:: valuesview[i]

      Return the value at position *i*.

      :rtype: value

   .. method:: valuesview.count(value)

      Return the number of occurrences of *value* in the set.

      :rtype: :class:`int`

   .. method:: valuesview.index(value)

      Return the smallest *k* such that :math:`valuesview[k] == x`.  Raises
      :exc:`ValueError` if *value* is not present.

      :rtype: :class:`int`

.. class:: ItemsView

   An ItemsView object is a dynamic view of the dictionary's ``(key,
   value)`` pairs, which means that when the dictionary changes, the
   view reflects those changes.

   :class:`ItemsView` implements the ItemsView, Set, and Sequence
   Abstract Base Class types.

   .. method:: len(itemsview)

      Return the number of entries in the dictionary.

      :rtype: :class:`int`

   .. method:: iter(itemsview)

      Return an iterator over the items in the dictionary.  Items are
      iterated over in sorted order of the keys.

      Iterating views while adding or deleting entries in the dictionary
      may raise a :exc:`RuntimeError` or fail to iterate over all
      entries.

      :rtype: iterator

   .. method:: reversed(itemsview)

      Return a reversed iterator over the items in the dictionary.

      Iterating views while adding or deleting entries in the dictionary
      may raise a :exc:`RuntimeError` or fail to iterate over all
      entries.

      :rtype: iterator

   .. method:: x in itemsview

      Return ``True`` iff *x* is one of the underlying dictionary's
      items.

      :rtype: :class:`bool`

   .. method:: itemsview[i]

      Return the ``(key, value)`` pair at position *i*.

      :rtype: item

   .. method:: itemsview & other

      Return the intersection of the items and the other object as
      a new set.

      :rtype: :class:`SortedSet`

   .. method:: itemsview | other

      Return the union of the items and the other object as a new set.

      :rtype: :class:`SortedSet`

   .. describe:: itemsview - other

      Return the difference between the items and the other object (all
      items that aren't in *other*) as a new set.

      :rtype: :class:`SortedSet`

   .. describe:: itemsview ^ other

      Return the symmetric difference (all elements either in the items
      or *other*, but not in both) of the items and the other object as
      a new set.

      :rtype: :class:`SortedSet`

   .. method:: itemsview.count(item)

      Return the number of occurrences of *item* in the set.

      :rtype: :class:`int`

   .. method:: itemsview.index(item, [start, [stop]])

      Return the smallest *k* such that :math:`itemsview[k] == x` and
      :math:`i <= k < j`.  Raises :exc:`KeyError` if *item* is not
      present.  *stop* defaults to the end of the set.  *start*
      defaults to the beginning.  Negative indexes are supported, as
      for slice indices.

      :rtype: :class:`int`

.. _Set: http://docs.python.org/release/3.1/library/collections.html#abcs-abstract-base-classes
.. _Sequence: http://docs.python.org/release/3.1/library/collections.html#abcs-abstract-base-classes
