Sorted Containers Release History
=================================

1.5.10 (2018-04-21)
-------------------

**Miscellaneous**

* Improved performance of islice(...) methods.

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
