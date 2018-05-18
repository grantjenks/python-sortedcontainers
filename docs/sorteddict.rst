.. automodule:: sortedcontainers.sorteddict


SortedDict
..........

.. autoclass:: sortedcontainers.SortedDict
   :show-inheritance:

   .. automethod:: __init__
   .. autoattribute:: key
   .. automethod:: __getitem__
   .. automethod:: __setitem__
   .. automethod:: __delitem__
   .. automethod:: __iter__
   .. automethod:: __len__
   .. automethod:: setdefault
   .. automethod:: update
   .. automethod:: clear
   .. automethod:: pop
   .. automethod:: popitem
   .. automethod:: __contains__
   .. automethod:: get
   .. automethod:: peekitem
   .. automethod:: keys
   .. automethod:: items
   .. automethod:: values
   .. automethod:: copy
   .. automethod:: fromkeys
   .. automethod:: __reversed__
   .. automethod:: __eq__
   .. automethod:: __ne__
   .. automethod:: __repr__
   .. automethod:: _check

   Sorted list methods (applies to keys):

   * :func:`SortedList.bisect_left`
   * :func:`SortedList.bisect_right`
   * :func:`SortedList.count`
   * :func:`SortedList.index`
   * :func:`SortedList.irange`
   * :func:`SortedList.islice`
   * :func:`SortedList._reset`

   Additional sorted list methods, if key-function used:

   * :func:`SortedKeyList.bisect_key_left`
   * :func:`SortedKeyList.bisect_key_right`
   * :func:`SortedKeyList.irange_key`


SortedKeysView
..............

.. autoclass:: sortedcontainers.SortedKeysView
   :show-inheritance:

   .. automethod:: __getitem__
   .. automethod:: __delitem__


SortedItemsView
...............

.. autoclass:: sortedcontainers.SortedItemsView
   :show-inheritance:

   .. automethod:: __getitem__


SortedValuesView
................

.. autoclass:: sortedcontainers.SortedValuesView
   :show-inheritance:

   .. automethod:: __getitem__
