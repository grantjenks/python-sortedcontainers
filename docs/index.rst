SortedContainers: Fast Pure-Python Sorted Container Types
=========================================================

SortedContainers is an :ref:`Apache2 Licensed <apache2>` containers library, written in Python, fast as C.

Python's standard library is great until you need a sorted container type. Many will attest that you can get really far without one, but the moment you **really need** a sorted list, dict, or set, you're faced with a dozen different implementations, most using C extensions without great documentation and benchmarking.

Things shouldn't be this way. Not in Python.

::

    >>> sl = sortedcontainers.SortedList(xrange(10000000)) # ten million integers
    >>> 1234567 in sl
    True
    >>> sl[7654321]
    7654321
    >>> sl.add(1234567)
    >>> sl.count(1234567)
    2
    >>> sl *= 3
    >>> len(sl)
    30000003

**Note:** don't try this at home without at least a gigabyte of memory. In Python an integer requires at least 12 bytes. SortedList will add about 4 bytes per object stored in the container. That's pretty hard to beat as it's the cost of a pointer to each object. It's also 66% less overhead than a typical binary tree implementation for which every node must store two pointers to children nodes.)

SortedContainers takes all of the work out of Python sorted types - making your deployment and use of Python easy. There's no need to install a C compiler or pre-build and distribute custom extensions. Performance is a feature and testing has 100% coverage with unit tests and hours of stress.

Feature Support
---------------

* Feature-rich
* Performance matters
* Pure-Python
* 100% test coverage
* Hours of stress testing
* Pragmatic design (e.g. SortedSet is a Python set with a SortedList index for iteration)
* Fully documented
* Benchmark comparison
* Developed on Python 2.7
* Tested on Python 2.6, 2.7, 3.2, and 3.3

User Guide
----------

Contents:

.. toctree::
   :maxdepth: 2
   sortedlist
   sorteddict
   sortedset
   implementation details

Useful Links
------------

// project page: grantjenks.com
// download: pypi
// browse source code: github
// issue tracker: github

Indices and Utilities
---------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
