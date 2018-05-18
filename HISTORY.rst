Sorted Containers Release History
=================================

.. contents::
   :depth: 1
   :local:

.. currentmodule:: sortedcontainers

2.0.1 (2018-05-18)
------------------

**Miscellaneous**

* Rename Github repo from `grantjenks/sorted_containers` to
  `grantjenks/python-sortedcontainers`.
* Fix broken links in documentation.

.. _v2:

2.0.0 (2018-05-18)
------------------

Version 2 represents a significant update to the source base. The code has been
refactored and modernized to embrace Python 3 semantics while also using
`autodoc` in Sphinx for more maintainable documentation. The core design and
algorithms are all the same. Sorted Containers still supports and is tested on
Python 2 but primary development is now on Python 3.6.

Version 2 is developed on the `master` branch in the source repository and
Version 1 of Sorted Containers will be maintained on branch `v1`.

Version 3 of Sorted Containers will be released sometime after January 1, 2020
and will drop support for Python 2.

At a high-level, changes can be categorized in three ways:

1. :class:`SortedList` methods `__setitem__`, `append`, `extend`, and `insert`
   all now raise :exc:`NotImplementedError`. Use `add` or `update`
   instead. Though it's possible to implement these methods, they were
   confusing, inefficient and wrongly used by some users. Sorted list
   implementations that need the functionality are encouraged to do so through
   subclassing. Branch `v1` contains a reference implementation.
2. :class:`SortedDict` now uses Python 3 semantics for dict views. The
   `iterkeys`, `iteritems`, `itervalues`, `viewkeys`, `viewitems`, and
   `viewvalues` methods have all been removed. Use the `keys`, `items`, or
   `values` methods which now return sorted dict views. :class:`SortedKeysView`
   has also replaced `SortedDict.iloc` as a better interface for indexing.
3. Method parameter names have changed to be more consistent with Python's
   built-in data types: `val` has changed to `value`, `idx` has changed to
   `index`, and `that` has changed to `other`.

**API Changes**

* :class:`SortedListWithKey` is deprecated. Use :class:`SortedKeyList` instead.
  The name `SortedListWithKey` remains as an alias for `SortedKeyList`. The
  alias will be removed in Version 3.
* `sortedcontainers.sortedlist.LOAD` has moved to
  `SortedList.DEFAULT_LOAD_FACTOR` so that derived classes can customize the
  value.
* `SortedList._half` and `SortedList._dual` have been removed. Use
  `SortedList._load` instead.
* :func:`SortedList.add` parameter `val` renamed to `value`.
* :func:`SortedList.__contains__` parameter `val` renamed to `value`.
* :func:`SortedList.discard` parameter `val` renamed to `value`.
* :func:`SortedList.remove` parameter `val` renamed to `value`.
* :func:`SortedList.__delitem__` parameter `idx` renamed to `index`.
* :func:`SortedList.__getitem__` parameter `idx` renamed to `index`.
* :func:`SortedList.__setitem__` now raises :exc:`NotImplementedError`. Use
  :func:`SortedList.__delitem__` and :func:`SortedList.add` instead.
* :func:`SortedList.bisect_left` parameter `val` renamed to `value`.
* :func:`SortedList.bisect_right` parameter `val` renamed to `value`.
* :func:`SortedList.bisect` parameter `val` renamed to `value`.
* :func:`SortedList.count` parameter `val` renamed to `value`.
* :func:`SortedList.append` now raises :exc:`NotImplementedError`. Use
  :func:`SortedList.add` instead.
* :func:`SortedList.extend` now raises :exc:`NotImplementedError`. Use
  :func:`SortedList.update` instead.
* :func:`SortedList.insert` now raises :exc:`NotImplementedError`. Use
  :func:`SortedList.add` instead.
* :func:`SortedList.pop` parameter `idx` renamed to `index`.
* :func:`SortedList.index` parameter `val` renamed to `value`.
* :func:`SortedList.__add__` parameter `that` renamed to `other`.
* :func:`SortedList.__iadd__` parameter `that` renamed to `other`.
* :func:`SortedList.__mul__` parameter `that` renamed to `num`.
* :func:`SortedList.__imul__` parameter `that` renamed to `num`.
* `SortedList._make_cmp` renamed to `SortedList.__make_cmp`.
* :func:`SortedKeyList.add` parameter `val` renamed to `value`.
* :func:`SortedKeyList.__contains__` parameter `val` renamed to `value`.
* :func:`SortedKeyList.discard` parameter `val` renamed to `value`.
* :func:`SortedKeyList.remove` parameter `val` renamed to `value`.
* :func:`SortedKeyList.bisect_left` parameter `val` renamed to `value`.
* :func:`SortedKeyList.bisect_right` parameter `val` renamed to `value`.
* :func:`SortedKeyList.bisect` parameter `val` renamed to `value`.
* :func:`SortedKeyList.count` parameter `val` renamed to `value`.
* :func:`SortedKeyList.append` now raises :exc:`NotImplementedError`. Use
  :func:`SortedKeyList.add` instead.
* :func:`SortedKeyList.extend` now raises :exc:`NotImplementedError`. Use
  :func:`SortedKeyList.update` instead.
* :func:`SortedKeyList.insert` now raises :exc:`NotImplementedError`. Use
  :func:`SortedKeyList.add` instead.
* :func:`SortedKeyList.index` parameter `val` renamed to `value`.
* :func:`SortedKeyList.__add__` parameter `that` renamed to `other`.
* :func:`SortedKeyList.__radd__` added.
* :func:`SortedKeyList.__iadd__` parameter `that` renamed to `other`.
* :func:`SortedKeyList.__mul__` parameter `that` renamed to `num`.
* :func:`SortedKeyList.__rmul__` added.
* :func:`SortedKeyList.__imul__` parameter `that` renamed to `num`.
* Removed `SortedDict.iloc`. Use :func:`SortedDict.keys` and
  :class:`SortedKeysView` instead.
* :func:`SortedDict.fromkeys` parameter `seq` renamed to `iterable`.
* :func:`SortedDict.keys` now returns :class:`SortedKeysView`.
* :func:`SortedDict.items` now returns :class:`SortedItemsView`.
* :func:`SortedDict.values` now returns :class:`SortedValuesView`.
* Removed `SortedDict.viewkeys`. Use :func:`SortedDict.keys` instead.
* Removed `SortedDict.viewitems`. Use :func:`SortedDict.items` instead.
* Removed `SortedDict.viewvalues`. Use :func:`SortedDict.values` instead.
* `SortedDict.iterkeys` removed. Use :func:`SortedDict.keys` instead.
* `SortedDict.iteritems` removed. Use :func:`SortedDict.items` instead.
* `SortedDict.itervalues` removed. Use :func:`SortedDict.values` instead.
* `SortedDict.popitem` now accepts an optional `index` argument. Default
  ``-1``.
* `sorteddict.KeysView` renamed to :class:`SortedKeysView`.
* `sorteddict.ItemsView` renamed to :class:`SortedItemsView`.
* `sorteddict.ValuesView` renamed to :class:`SortedValuesView`.
* Sorted dict views rely on collections abstract base classes: dict views and
  sequence. The :func:`SortedKeysView.__getitem__`,
  :func:`SortedItemsView.__getitem__`, and :func:`SortedValuesView.__getitem__`
  methods are implemented and optimized. All other mixin methods use the
  default implementation provided by the base class. Prefer :class:`SortedDict`
  methods to view methods when possible.
* `SortedSet._make_cmp` renamed to `SortedSet.__make_cmp`.
* :func:`SortedSet.symmetric_difference` parameter `that` renamed to `other`.
* :func:`SortedSet.symmetric_difference_update` parameter `that` renamed to
  `other`.

**Miscellaneous**

* Sphinx `autodoc` now used for API documentation.
* All benchmarks now run on CPython 3.6 unless otherwise noted.
* Testing now uses `pytest` rather than `nose`.
* AppVeyor CI testing added.
* Updated versions of alternative implementations.

1.5.10 (2018-04-21)
-------------------

**Miscellaneous**

* Improved performance of irange(...) and islice(...) methods.

1.5.9 (2017-12-08)
------------------

**Miscellaneous**

* Dropped CPython 2.6 testing.

1.5.8 (2017-12-08)
------------------

**Bugfixes**

* Added ``SortedList.reverse`` to override ``MutableSequence.reverse`` and
  raise ``NotImplementedError``.

1.5.7 (2016-12-22)
------------------

**Bugfixes**

* Changed ``SortedList.__setitem__`` to support slices with stop less than
  start and step equal one.

1.5.6 (2016-12-09)
------------------

**Bugfixes**

* Changed ``SortedList.__setitem__`` to support slices that alias itself.


1.5.5 (2016-12-05)
------------------

**Bugfixes**

* Changed ``SortedList.extend`` to support empty iterables.

1.5.4 (2016-10-16)
------------------

**Bugfixes**

* Changed ``SortedList.__new__`` to call ``SortedListWithKey.__init__`` once
  instead of twice.

1.5.3 (2016-06-01)
------------------

**Miscellaneous**

* Updated documentation with PyCon 2016 Talk.

1.5.2 (2016-05-28)
------------------

**API Changes**

* Added ``SortedDict.peekitem`` method.

1.5.1 (2016-05-26)
------------------

**Miscellaneous**

* Added support for PyLint and minor source changes.
* Dropped Python 3.2 support from tox testing due to virtualenv limitations.

1.5.0 (2016-05-26)
------------------

**Miscellaneous**

* Added Performance at Scale documentation.

1.4.3 (2015-12-03)
------------------

**Miscellaneous**

* Updated documentation with SF Python 2015 Holiday Meetup Talk.

1.4.2 (2015-10-20)
------------------

**API Changes**

* Changed ``SortedList`` initializer to support key-argument callable and
  automatically return ``SortedListWithKey`` when present.
* Changed ``SortedListWithKey`` to inherit from ``SortedList``.
* Changed ``SortedSet.__ior__`` to call `update` rather than `union`.
* Changed SortedList comparison to match Sequence semantics as described in
  CPython Language Reference Section 5.9.
* Changed SortedSet comparison to raise NotImplemented on type mismatch.
* Removed SortedList.as_list method. Use ``list(sorted_list)`` instead.
* Removed SortedList._slice method. Use ``slice.indices`` instead.
* Added private references to public methods for internal use to ease
  method over-loading.

**Bugfixes**

* Changed sorteddict.ValuesView.count to correctly reference sorted dictionary.

**Improvements**

* ``SortedList.__getitem__`` now 35% faster for indexing at beginning and end.
* ``SortedList.pop`` now 35% faster by inlining fast-paths.
* ``del sorted_list[:]`` now calls `clear` and is much faster.
* ``sorted_list[:] = values`` now calls `clear` and `update` and is much faster.

**Miscellaneous**

* Added Python 3.5 support in tox testing.
* Added discussion of `ruamel.ordereddict.sorteddict` to performance
  documentation.
* Merged file ``sortedlistwithkey.py`` into ``sortedlist.py``.

0.9.6 (2015-06-22)
------------------

**API Changes**

* Added ``islice`` method to sorted list, dict, and set types.
* Added ``irange`` and ``irange_key`` method to sorted list, dict, and set
  types.

0.9.5 (2015-03-16)
------------------

**API Changes**

* Added ``bisect_key`` methods to sorted list, dict, and set types.
* Added ``last=True`` argument to ``SortedDict.popitem``.

0.9.4 (2014-12-04)
------------------

**Bugfixes**

* Added implementation and testing for Python pickle module.

0.9.3 (2014-11-30)
------------------

**API Changes**

* Removed ``SortedListWithKeyPair`` type.

**Improvements**

* Changed type references to ``self.__class__`` as able.

0.9.2 (2014-10-20)
------------------

**API Changes**

* Removed ``value_orderable`` argument from ``SortedListWithKey`` initializer.
* Added key-callable argument to ``SortedDict`` initializer.
* Added key-callable argument to ``SortedSet`` initializer.

**Improvements**

* Changed ``SortedDict`` to inherit directly from ``dict``.

**Miscellaneous**

* Added PyPy3 support to tox testing.
* Added ``SortedListWithKey`` to sorted list performance comparison
  documentation.

0.9.1 (2014-09-20)
------------------

**Bugfixes**

* Changed ``SortedList.__setitem__`` with slices to correctly update internal
  "maxes" index.

0.9.0 (2014-09-17)
------------------

**API Changes**

* Added ``__ior__``, ``__iand__``, ``__isub__``, and ``__ixor__`` methods to
  ``SortedSet`` interface.

**Improvements**

* Changed position-based indexing to use dense tree-based index.

**Miscellaneous**

* Added workload-based performance comparison for sorted list: Priority Queue,
  Multiset, etc.

0.8.5 (2014-08-11)
------------------

**Bugfixes**

* Changed copy methods to make shallow copies: values are not copied, only
  references to values are copied.

**Miscellaneous**

* Added load-factor performance comparison documentation.

0.8.4 (2014-07-29)
------------------

**API Changes**

* Added ``value_orderable`` parameter to ``SortedListWithKey`` to support
  incomparable value types.

**Bugfixes**

* Changed ``repr`` methods to prevent infinite recursion and allow easier
  subclassing.

0.8.3 (2014-07-07)
------------------

**Miscellaneous**

* Added more testing for sorted lists with key-callable argument.

0.8.2 (2014-06-13)
------------------

**API Changes**

* Added ``SortedListWithKey`` type with implementation based on
  ``(key, value)`` tuples.

0.8.1 (2014-05-08)
------------------

**Bugfixes**

* Added contains-key check in sorted dict equality comparisons.

**Miscellaneous**

* Added Python runtime comparison to documentation.
* Added sorted dict and set comparison to benchmark documentation.
* Added Travis-CI testing.

0.8.0 (2014-04-08)
------------------

**API Changes**

* Added ``bisect`` methods from ``SortedList`` to ``SortedDict`` interface.

0.7.0 (2014-04-02)
------------------

**Miscellaneous**

* Added Banyan module to benchmark documentation.

0.6.0 (2014-03-18)
------------------

**Miscellaneous**

* Added testing support for CPython 2.6, 2.7, 3.2, and 3.3 with full coverage.

0.5.0 (2014-03-14)
------------------

* Initial release of sorted list, dict, and set types.
