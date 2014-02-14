Introduction
============

Installation
------------

This part of the documentation covers the installation of SortedContainers.
The first step to using any software package is getting it properly installed.

Distribute & Pip
................

Installing SortedContainers is simple with `pip <http://www.pip-installer.org/>`_::

    > pip install sortedcontainers

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    > easy_install sortedcontainers

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.

Get the Code
............

SortedContainers is actively developed on GitHub, where the code is
`always available <https://github.com/grantjenks/sortedcontainers>`_.

You can either clone the public repository::

    > git clone git://github.com/grantjenks/sortedcontainers.git

Download the `tarball <https://github.com/grantjenks/sortedcontainers/tarball/master>`_::

    > curl -OL https://github.com/grantjenks/sortedcontainers/tarball/master

Or, download the `zipball <https://github.com/grantjenks/sortedcontainers/zipball/master>`_::

    > curl -OL https://github.com/grantjenks/sortedcontainers/zipball/master

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    > python setup.py install

SortedList
----------

A SortedList is a finite sequence in which an order is imposed on the elements
according to their inequality relation to each other. As with Python's built-in
list data type, SortedList supports duplicate elements and fast random-access
indexing. A SortedList may never contain its elements out of order.

    >>> from sortedcontainers import SortedList
    >>> l = SortedList()

Elements may be added to a SortedList using either :ref:`add <SortedList.add>`
or :ref:`update <SortedList.update>`. When doing so, the list remains sorted.

    >>> l.update([0, 4, 1, 3, 2])
    >>> l.index(3)
    3
    >>> l.add(5)
    >>> l[-1]
    5

Elements may also be inserted into a SortedList using :ref:`append
<SortedList.append>`, :ref:`__setitem__ <SortedList.__setitem__>`, :ref:`insert
<SortedList.insert>`, or :ref:`extend <SortedList.extend>`. These functions
follow the programmer's directive to insert the element(s) at a specific
location. Inserting an element out of order in this way will cause a ValueError.

    >>> l[:] = [0, 1, 2, 3, 4]
    >>> l.append(5)
    >>> l.insert(0, 0)
    >>> l.extend(range(6, 10))
    >>> print(','.join(map(str, l)))
    0,0,1,2,3,4,5,6,7,8,9
    >>> l.insert(10, 5)
    ValueError

Removing elements from a SortedList is done with :ref:`discard
<SortedList.discard>`, :ref:`remove <SortedList.remove>`, :ref:`__delitem__
<SortedList.__delitem__`, or :ref:`pop <SortedList.pop>`. These functions work
identically to their list counterpart.

    >>> l[:] = range(10)
    >>> del l[-9:-3:3]
    >>> l.discard(0)
    >>> l.remove(5)
    >>> l.pop()
    9
    >>> len(l)
    5

Because the SortedList maintains its elements in sorted order, several functions
can be computed efficiently using binary-search. Those functions are :ref:`index
<SortedList.index>`, :ref:`count <SortedList.count>`, :ref:`bisect
<SortedList.bisect>`, :ref:`bisect_left <SortedList.bisect>`, and
:ref:`bisect_right <SortedList.bisect>`.

    >>> l.clear()
    >>> l.update(range(1000000))
    >>> l.index(123456)
    123456
    >>> l.count(654321)
    1
    >>> l.bisect(123456.7)
    123457

SortedList also works efficiently with other sequence data types. :ref:`Addition
<SortedList.__add__>`, :ref:`multiplication <SortedList.__mul__>`, and
:ref:`comparison <SortedList.__eq__>` works with any iterable.

    >>> l[:] = range(10)
    >>> l += range(10)
    >>> l *= 2
    >>> l >= [0, 0, 0, 0]
    True
    >>> del l[::4]
    >>> del l[::3]
    >>> del l[::2]
    >>> l == range(10)
    True

For more details, refer to the :doc:`SortedList API documentation <sortedlist>`.

SortedSet
---------

SortedDict
----------
