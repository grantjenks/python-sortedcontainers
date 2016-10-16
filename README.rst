Python SortedContainers
=======================

.. image:: https://api.travis-ci.org/grantjenks/sorted_containers.svg
    :target: http://www.grantjenks.com/docs/sortedcontainers/

`SortedContainers`_ is an Apache2 licensed `sorted collections library`_,
written in pure-Python, and fast as C-extensions.

Python's standard library is great until you need a sorted collections
type. Many will attest that you can get really far without one, but the moment
you **really need** a sorted list, dict, or set, you're faced with a dozen
different implementations, most using C-extensions without great documentation
and benchmarking.

In Python, we can do better. And we can do it in pure-Python!

.. code-block:: python

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

**Note:** don't try this without at least a half gigabyte of memory. In Python
an integer requires about 24 bytes. SortedList will add about 8 bytes per
object stored in the container. That's pretty hard to beat as it's the cost of
a pointer to each object. It's also 66% less overhead than a typical binary
tree implementation (e.g. red-black tree, avl tree, aa tree, splay tree, treap,
etc.) for which every node must also store two pointers to children nodes.

`SortedContainers`_ takes all of the work out of Python sorted collections -
making your deployment and use of Python easy. There's no need to install a C
compiler or pre-build and distribute custom extensions. Performance is a
feature and testing has 100% coverage with unit tests and hours of stress.

.. _`SortedContainers`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`sorted collections library`: http://www.grantjenks.com/docs/sortedcontainers/

Testimonials
------------

**Alex Martelli**, `Wikipedia`_

Good stuff! ... I like the `simple, effective implementation`_ idea of splitting
the sorted containers into smaller "fragments" to avoid the O(N) insertion costs.

.. _`Wikipedia`: http://en.wikipedia.org/wiki/Alex_Martelli
.. _`simple, effective implementation`: http://www.grantjenks.com/docs/sortedcontainers/implementation.html

**Jeff Knupp**, `Review of SortedContainers`_

That last part, "fast as C-extensions," was difficult to believe. I would need
some sort of `Performance Comparison`_ to be convinced this is true. The author
includes this in the docs. It is.

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
- Tested on CPython 2.6, 2.7, 3.2, 3.3, 3.4, 3.5 and PyPy 5.1+, PyPy3 2.4+

Quickstart
----------

Installing `SortedContainers`_ is simple with
`pip <http://www.pip-installer.org/>`_::

    $ pip install sortedcontainers

You can access documentation in the interpreter with Python's built-in help
function:

.. code-block:: python

    >>> from sortedcontainers import SortedList, SortedSet, SortedDict
    >>> help(SortedList)

Documentation
-------------

Complete documentation including performance comparisons is available at
http://www.grantjenks.com/docs/sortedcontainers/ .

User Guide
..........

For those wanting more details, this part of the documentation describes
introduction, implementation, performance, and development.

- `Introduction`_
- `Performance Comparison`_
- `Load Factor Performance Comparison`_
- `Runtime Performance Comparison`_
- `Simulated Workload Performance Comparison`_
- `Implementation Details`_
- `Performance at Scale`_
- `Developing and Contributing`_

.. _`Introduction`: http://www.grantjenks.com/docs/sortedcontainers/introduction.html
.. _`Performance Comparison`: http://www.grantjenks.com/docs/sortedcontainers/performance.html
.. _`Load Factor Performance Comparison`: http://www.grantjenks.com/docs/sortedcontainers/performance-load.html
.. _`Runtime Performance Comparison`: http://www.grantjenks.com/docs/sortedcontainers/performance-runtime.html
.. _`Simulated Workload Performance Comparison`: http://www.grantjenks.com/docs/sortedcontainers/performance-workload.html
.. _`Implementation Details`: http://www.grantjenks.com/docs/sortedcontainers/implementation.html
.. _`Performance at Scale`: http://www.grantjenks.com/docs/sortedcontainers/performance-scale.html
.. _`Developing and Contributing`: http://www.grantjenks.com/docs/sortedcontainers/development.html

API Documentation
.................

If you are looking for information on a specific function, class or method, this
part of the documentation is for you.

- `SortedList`_
- `SortedListWithKey`_
- `SortedDict`_
- `SortedSet`_

.. _`SortedList`: http://www.grantjenks.com/docs/sortedcontainers/sortedlist.html
.. _`SortedListWithKey`: http://www.grantjenks.com/docs/sortedcontainers/sortedlistwithkey.html
.. _`SortedDict`: http://www.grantjenks.com/docs/sortedcontainers/sorteddict.html
.. _`SortedSet`: http://www.grantjenks.com/docs/sortedcontainers/sortedset.html

Talks
-----

- `Python Sorted Collections | PyCon 2016 Talk`_
- `SF Python Holiday Party 2015 Lightning Talk`_
- `DjangoCon 2015 Lightning Talk`_

.. _`Python Sorted Collections | PyCon 2016 Talk`: http://www.grantjenks.com/docs/sortedcontainers/pycon-2016-talk.html
.. _`SF Python Holiday Party 2015 Lightning Talk`: http://www.grantjenks.com/docs/sortedcontainers/sf-python-2015-lightning-talk.html
.. _`DjangoCon 2015 Lightning Talk`: http://www.grantjenks.com/docs/sortedcontainers/djangocon-2015-lightning-talk.html

Contribute
----------

Collaborators are welcome!

#. Check for open issues or open a fresh issue to start a discussion around a
   bug.  There is a Contributor Friendly tag for issues that should be used by
   people who are not very familiar with the codebase yet.
#. Fork the `SortedContainers repository
   <https://github.com/grantjenks/sorted_containers>`_ on GitHub and start
   making your changes to a new branch.
#. Write a test which shows that the bug was fixed.
#. Send a pull request and bug the maintainer until it gets merged and
   published.

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

SortedContainers License
------------------------

Copyright 2014-2016 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
