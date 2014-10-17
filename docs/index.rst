SortedContainers
================

SortedContainers is an :ref:`Apache2 Licensed <apache2>` containers library,
written in pure-Python, and fast as C-extensions.

Python's standard library is great until you need a sorted container type. Many
will attest that you can get really far without one, but the moment you **really
need** a sorted list, dict, or set, you're faced with a dozen different
implementations, most using C-extensions without great documentation and
benchmarking.

Things shouldn't be this way. Not in Python.

::

    >>> sl = sortedcontainers.SortedList(xrange(10000000))
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

**Note:** don't try this at home without at least a gigabyte of memory. In
Python an integer requires at least 12 bytes. SortedList will add about 4
bytes per object stored in the container. That's pretty hard to beat as it's
the cost of a pointer to each object. It's also 66% less overhead than a
typical binary tree implementation for which every node must also store two
pointers to children nodes.)

SortedContainers takes all of the work out of Python sorted types - making your
deployment and use of Python easy. There's no need to install a C compiler or
pre-build and distribute custom extensions. Performance is a feature and testing
has 100% coverage with unit tests and hours of stress.

Testimonials
------------

**Alex Martelli**, `Wikipedia`_

Good stuff! ... I like the :doc:`simple, effective implementation
<implementation>` idea of splitting the sorted containers into smaller
"fragments" to avoid the O(N) insertion costs.

.. _`Wikipedia`: http://en.wikipedia.org/wiki/Alex_Martelli

**Jeff Knupp**, `Review of SortedContainers`_

That last part, "fast as C-extensions," was difficult to believe. I would need
some sort of :doc:`performance comparison <performance>` to be convinced this is
true. The author includes this in the docs. It is.

.. _`JeffKnupp.com`: http://jeffknupp.com/
.. _`Review of SortedContainers`: http://reviews.jeffknupp.com/reviews/sortedcontainers/3/

**Kevin Samuel**, `Formations Python`_

I'm quite amazed, not just by the code quality (it's incredibly
readable and has more comment than code, wow), but the actual
amount of work you put at stuff that is *not* code:
documentation, benchmarking, implementation explanations. Even
the git log is clean and the unit tests run out of the box on
Python 2 and 3.

.. _`Formations Python`: http://formationspython.com/

**Mark Summerfield**, a short plea for `Python Sorted Collections`_

Python's "batteries included" standard library seems to have a battery
missing. And the argument that "we never had it before" has worn thin. It is
time that Python offered a full range of collection classes out of the box,
including sorted ones.

.. _`Python Sorted Collections`: http://www.qtrac.eu/pysorted.html

Features
--------

- Pure-Python
- Fully documented
- Benchmark comparison
- 100% test coverage
- Hours of stress testing
- Performance matters (often faster than C implementations)
- Compatible API (nearly identical to popular blist and rbtree modules)
- Feature-rich (e.g. get the five largest keys in a sorted dict: d.iloc[-5:])
- Pragmatic design (e.g. SortedSet is mostly a Python set with a SortedList
  index)
- Developed on Python 2.7
- Tested on CPython 2.6, 2.7, 3.2, 3.3, 3.4, PyPy 2.2+ and PyPy3 2.3.1+.

Quickstart
----------

Installing SortedContainers is simple with
`pip <http://www.pip-installer.org/>`_::

    > pip install sortedcontainers

You can access documentation in the interpreter with Python's built-in help
function:

    >>> from sortedcontainers import SortedList, SortedSet, SortedDict
    >>> help(SortedList)

User Guide
----------

For those wanting more details, this part of the documentation describes
introduction, implementation, performance, and development.

.. toctree::
   :maxdepth: 1

   introduction
   performance
   performance-load
   performance-runtime
   performance-workload
   implementation
   development

API Documentation
-----------------

If you are looking for information on a specific function, class or method, this
part of the documentation is for you.

.. toctree::
   :maxdepth: 1

   sortedlist
   sortedlistwithkey
   sorteddict
   sortedset

Useful Links
------------

- `SortedContainers Module @ GrantJenks.com`_
- `SortedContainers @ PyPI`_
- `SortedContainers @ Github`_
- `Issue Tracker`_

.. _`SortedContainers Module @ GrantJenks.com`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`SortedContainers @ PyPI`: https://pypi.python.org/pypi/sortedcontainers
.. _`SortedContainers @ Github`: https://github.com/grantjenks/sorted_containers
.. _`Issue Tracker`: https://github.com/grantjenks/sorted_containers/issues

Indices and Utilities
---------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`apache2`:

Apache2 License
---------------

A large number of open source projects you find today are `GPL Licensed`_.
A project that is released as GPL cannot be used in any commercial product
without the product itself also being offered as open source.

The MIT, BSD, ISC, and Apache2 licenses are great alternatives to the GPL
that allow your open-source software to be used freely in proprietary,
closed-source software.

SortedContainers is released under terms of `Apache2 License`_.

.. _`GPL Licensed`: http://www.opensource.org/licenses/gpl-license.php
.. _`Apache2 License`: http://opensource.org/licenses/Apache-2.0


SortedContainers License
------------------------

    .. include:: ../LICENSE
