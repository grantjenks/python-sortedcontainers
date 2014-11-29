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
`always available <https://github.com/grantjenks/sorted_containers>`_.

You can either clone the public repository::

    > git clone git://github.com/grantjenks/sorted_containers.git

Download the `tarball <https://github.com/grantjenks/sorted_containers/tarball/master>`_::

    > curl -OL https://github.com/grantjenks/sorted_containers/tarball/master

Or, download the `zipball <https://github.com/grantjenks/sorted_containers/zipball/master>`_::

    > curl -OL https://github.com/grantjenks/sorted_containers/zipball/master

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    > python setup.py install

SortedList
----------

A SortedList is a finite sequence in which an order is imposed on the elements
according to their ordered relation to each other. As with Python's built-in
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
<SortedList.__delitem__>`, or :ref:`pop <SortedList.pop>`. These functions work
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

SortedListWithKey
-----------------

The SortedContainers project also maintains a specialized SortedList-like type
that accepts a key-parameter as found with Python's built-in *sorted* function.
A SortedListWithKey provides the same functionality as a SortedList but
maintains the order of contained values based on the applied key-function. This
simplifies the pattern of boxing/un-boxing which would otherwise be required.

    >>> from sortedcontainers import SortedListWithKey
    >>> l = SortedListWithKey(key=lambda val: -val)

The key function extracts a comparison key for ordering items in the list. In
our example above we apply the negation operator. Doing so would maintain a list
of integers in reverse.

For more details, refer to the :doc:`SortedListWithKey API documentation <sortedlistwithkey>`.

SortedDict
----------

A SortedDict is a container of key-value pairs in which an order is imposed on
the keys according to their ordered relation to each other. As with Python's
built-in dict data type, SortedDict supports fast insertion, deletion, and
lookup by key. Iterating a SortedDict yields the keys in sorted order. The api
strives to be as similar to the built-in dict type as possible.

    >>> from sortedcontainers import SortedDict
    >>> d = SortedDict()
    >>> d.update(alice=518, bob=285, carol=925, dave=376, ellen=874)
    >>> print(''.join(key[0] for key in d))
    abcde
    >>> d['frank'] = 102
    >>> d['bob'] = 341
    >>> del d['frank']
    >>> 'ellen' in d
    True
    >>> d.get('frank', 0)
    0
    >>> d.pop()
    'ellen'

SortedDict also supports key, value, and item iteration/views according to the
Python version. (Python 2.7 and higher supports views while Python 2.6 supports
only iteration.) View operations like :ref:`and <KeysView.and>`,
:ref:`or <KeysView.or>`, :ref:`sub <KeysView.sub>`, and
:ref:`xor <KeysView.xor>` return a SortedSet container.

    >>> d.clear()
    >>> d.update(list(enumerate('0123456789')))
    >>> keys = d.keys()
    >>> len(keys)
    10
    >>> d[-1] = '-1'
    >>> len(keys)
    11
    >>> s = SortedDict([(1, '1'), (2, '2'), (3, '3'), (10, '10')])
    >>> s.keys() & keys
    SortedSet([1, 2, 3])

In addition to the normal dictionary operations, SortedDict supports fast
:ref:`indexing with iloc<SortedDict.iloc>` and :ref:`key index
lookup<SortedDict.index>`. Using indexing, you can quickly lookup the nth key in
iteration. These utilities are not common in other implementations but can be
extremely useful. Indexing also supports slice notation.

    >>> d = SortedDict(b=2, d=4, c=3, e=5, a=1)
    >>> d.iloc[0]
    'a'
    >>> d.iloc[-1]
    'e'
    >>> d.iloc[-3:]
    ['c', 'd', 'e']
    >>> d.index('c')
    2

For more details, refer to the :doc:`SortedDict API documentation <sorteddict>`.

SortedSet
---------

A :doc:`SortedSet<sortedset>` is a collection of distinct objects in which an
order is imposed on the members according to their ordered relation to each
other. The API is similar to the :doc:`SortedList<sortedlist>` and built-in set
containers. Iterating a SortedSet yields the items in sorted order.

    >>> from sortedcontainers import SortedSet
    >>> s = SortedSet([3, 1, 0, 2])
    >>> list(s)
    [0, 1, 2, 3]

Like the built-in set container type, SortedSet supports
:ref:`difference<SortedSet.difference>`,
:ref:`intersection<SortedSet.intersection>`,
:ref:`symmetric_difference<SortedSet.symmetric_difference>`, and
:ref:`union<SortedSet.union>` operations along with their _update counterparts.

    >>> s.clear()
    >>> s.add(-1)
    >>> s.update(xrange(10))
    >>> 5 in s
    True
    >>> s - [1, 2, 3]
    SortedSet([-1, 0, 4, 5, 6, 7, 8, 9])
    >>> s & [-3, -2, -1, 0]
    SortedSet([-1, 0])
    >>> s > [1, 2, 3]
    True

Adding and removing elements works the same as with the SortedList container
although position-specifying updates are not permitted.Unlike the built-in set
type, SortedSet has full indexing support for
:ref:`set[index]<SortedSet.__getitem__>` and :ref:`del
set[index]<SortedSet.__delitem__>` operations.

    >>> s.clear()
    >>> s.update(xrange(100))
    >>> s[5]
    5
    >>> s[2:10:2]
    SortedSet([2, 4, 6, 8])
    >>> del s[3:15:3]
    >>> len(s)
    96

For more details, refer to the :doc:`SortedSet API documentation<sortedset>`.
