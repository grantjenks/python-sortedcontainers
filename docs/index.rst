SortedContainers
================

`SortedContainers`_ is an Apache2 licensed sorted collections library, written
in pure-Python, and fast as C-extensions.

Python's standard library is great until you need a sorted collections
type. Many will attest that you can get really far without one, but the moment
you **really need** a sorted list, dict, or set, you're faced with a dozen
different implementations, most using C-extensions without great documentation
and benchmarking.

In Python, we can do better. And we can do it in pure-Python!

::

    >>> sl = sortedcontainers.SortedList(range(int(1e7)))
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

*Note:* The snippet above requires at least a half gigabyte of memory. In
64-bit versions of CPython an integer requires about 24 bytes. SortedList will
add about 8 bytes per object stored in the container. That's pretty hard to
beat as it's the cost of a pointer to each object. It's also 66% less overhead
than a typical binary tree implementation (e.g. red-black tree, avl tree, aa
tree, splay tree, treap, etc.) for which every node must also store two
pointers to children nodes.

`SortedContainers`_ takes all of the work out of Python sorted collections --
making your deployment and use of Python easy. There's no need to install a C
compiler or pre-build and distribute custom extensions. Performance is a
feature and testing has 100% coverage with unit tests and hours of stress.

Testimonials
------------

**Alex Martelli**, `Wikipedia`_

Good stuff! ... I like the :doc:`simple, effective implementation
<implementation>` idea of splitting the sorted containers into smaller
"fragments" to avoid the O(N) insertion costs.

.. _`Wikipedia`: http://en.wikipedia.org/wiki/Alex_Martelli

**Jeff Knupp**, `Review of SortedContainers`_

That last part, "fast as C-extensions," was difficult to believe. I would need
some sort of :doc:`performance comparison <performance>` to be convinced this
is true. The author includes this in the docs. It is.

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
- Benchmark comparison (alternatives, runtimes, load-factors)
- 100% test coverage
- Hours of stress testing
- Performance matters (often faster than C implementations)
- Compatible API (nearly identical to popular blist and rbtree modules)
- Feature-rich (e.g. get the five largest keys in a sorted dict: d.iloc[-5:])
- Pragmatic design (e.g. SortedSet is a Python set with a SortedList index)
- Developed on Python 2.7
- Tested on CPython 2.7, 3.2, 3.3, 3.4, 3.5, 3.6 and PyPy, PyPy3

Quickstart
----------

Installing `SortedContainers`_ is simple with
`pip <http://www.pip-installer.org/>`_::

    $ pip install sortedcontainers

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
   performance-scale
   development
   history

API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 1

   sortedlist
   sortedlistwithkey
   sorteddict
   sortedset

Talks
-----

.. toctree::
   :maxdepth: 1

   pycon-2016-talk
   sf-python-2015-lightning-talk
   djangocon-2015-lightning-talk

Useful Links
------------

- `SortedContainers Documentation`_
- `SortedContainers at PyPI`_
- `SortedContainers at Github`_
- `SortedContainers Issue Tracker`_

.. _`SortedContainers Documentation`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`SortedContainers at PyPI`: https://pypi.python.org/pypi/sortedcontainers
.. _`SortedContainers at Github`: https://github.com/grantjenks/sorted_containers
.. _`SortedContainers Issue Tracker`: https://github.com/grantjenks/sorted_containers/issues

Indices and Utilities
---------------------

* :ref:`genindex`
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

`SortedContainers`_ is released under terms of the `Apache2 License`_.

.. _`GPL Licensed`: http://www.opensource.org/licenses/gpl-license.php
.. _`Apache2 License`: http://opensource.org/licenses/Apache-2.0


SortedContainers License
------------------------

.. include:: ../LICENSE

.. _`SortedContainers`: http://www.grantjenks.com/docs/sortedcontainers/
