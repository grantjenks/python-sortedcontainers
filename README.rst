SortedContainers
================

.. image:: https://api.travis-ci.org/grantjenks/sorted_containers.svg
    :target: http://www.grantjenks.com/docs/sortedcontainers/

SortedContainers is an Apache2 licensed containers library, written in
pure-Python, and fast as C-extensions.

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
pointers to children nodes.

SortedContainers takes all of the work out of Python sorted types - making your
deployment and use of Python easy. There's no need to install a C compiler or
pre-build and distribute custom extensions. Performance is a feature and testing
has 100% coverage with unit tests and hours of stress.

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
- Tested on Python 2.6, 2.7, 3.2, 3.3, and 3.4

Quickstart
----------

Installing SortedContainers is simple with
`pip <http://www.pip-installer.org/>`_::

    > pip install sortedcontainers

You can access documentation in the interpreter with Python's built-in help
function:

::

    >>> from sortedcontainers import SortedList, SortedSet, SortedDict
    >>> help(SortedList)

Documentation
-------------

Complete documentation including performance comparisons is available at
http://www.grantjenks.com/docs/sortedcontainers/ .

Contribute
----------

Collaborators are welcome!

#. Check for open issues or open a fresh issue to start a discussion around a
   bug.  There is a Contributor Friendly tag for issues that should be used by
   people who are not very familiar with the codebase yet.
#. Fork `the repository <https://github.com/grantjenks/sorted_containers>`_ on
   GitHub and start making your changes to a new branch.
#. Write a test which shows that the bug was fixed.
#. Send a pull request and bug the maintainer until it gets merged and
   published. :)

Useful Links
------------

- `SortedContainers Project @ GrantJenks.com`_
- `SortedContainers @ PyPI`_
- `SortedContainers @ Github`_
- `Issue Tracker`_

.. _`SortedContainers Project @ GrantJenks.com`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`SortedContainers @ PyPI`: https://pypi.python.org/pypi/sortedcontainers
.. _`SortedContainers @ Github`: https://github.com/grantjenks/sorted_containers
.. _`Issue Tracker`: https://github.com/grantjenks/sorted_containers/issues

SortedContainers License
------------------------

Copyright 2014 Grant Jenks

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
