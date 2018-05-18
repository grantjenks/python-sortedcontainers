Sorted Containers Introduction
==============================

.. currentmodule:: sortedcontainers

.. contents::
   :local:


Installation
------------

The first step to using any software library is getting it properly installed.
There are several ways to install :doc:`Sorted Containers<index>`.

The recommended way to install :doc:`Sorted Containers<index>` is using the
`pip`_ command::

    $ python3 -m pip install sortedcontainers

You may also choose instead to use the newer `pipenv`_ command::

    $ pipenv install sortedcontainers

These commands will install the latest version of :doc:`Sorted
Containers<index>` from the `Python Package Index`_.

:doc:`Sorted Containers<index>` is actively developed on GitHub, where the code
is `open source`_. You may choose to install directly from the source
repository. First, you will need a copy of the sources. The recommended way to
get a copy of the source repository is to clone the repository from GitHub::

    $ git clone git://github.com/grantjenks/python-sortedcontainers.git

You may also choose instead to download the `Sorted Containers tarball`_ or
download the `Sorted Containers zipball`_.

Once you have a copy of the sources, you can embed it in your Python package,
or install it into your site-packages using the command::

    $ python3 setup.py install

:doc:`Sorted Containers<index>` is available in Debian distributions as
`python3-sortedcontainers` and `python-sortedcontainers`.

:doc:`Sorted Containers<index>` is looking for a CentOS/RPM package
maintainer. If you can help, please open an issue in the `Sorted Containers
Issue Tracker`_.

.. _`pip`: https://pypi.org/project/pip/
.. _`pipenv`: https://pypi.org/project/pipenv/
.. _`Python Package Index`: https://pypi.org/project/sortedcontainers/
.. _`open source`: https://github.com/grantjenks/python-sortedcontainers
.. _`Sorted Containers tarball`: https://github.com/grantjenks/python-sortedcontainers/tarball/master
.. _`Sorted Containers zipball`: https://github.com/grantjenks/python-sortedcontainers/zipball/master
.. _`Sorted Containers Issue Tracker`: https://github.com/grantjenks/python-sortedcontainers/issues


Sorted List
-----------

At the core of :doc:`Sorted Containers<index>` is the mutable sequence data
type :class:`SortedList`. The :class:`SortedList` maintains its values in
ascending sort order. As with Python's built-in list data type,
:class:`SortedList` supports duplicate elements and fast random-access
indexing.

    >>> from sortedcontainers import SortedList
    >>> sl = SortedList()

Values may be added to a :class:`SortedList` using either
:func:`SortedList.update` or :func:`SortedList.add`. When doing so, the list
remains sorted.

    >>> sl.update([5, 1, 3, 4, 2])
    >>> sl
    SortedList([1, 2, 3, 4, 5])
    >>> sl.add(0)
    >>> sl
    SortedList([0, 1, 2, 3, 4, 5])

Several methods may be used to remove elements by value or by index. The
methods :func:`SortedList.discard` and :func:`SortedList.remove` remove
elements by value. And the methods :func:`SortedList.pop` and
:func:`SortedList.__delitem__` remove elements by index. All values may be
removed using :func:`SortedList.clear`.

    >>> sl.remove(0)
    >>> sl.discard(1)
    >>> sl
    SortedList([2, 3, 4, 5])
    >>> sl.pop()
    5
    >>> del sl[1]
    >>> sl
    SortedList([2, 4])
    >>> sl.clear()

Because :class:`SortedList` is sorted, it supports efficient lookups by value
or by index. When accessing values by index, the :class:`SortedList` can be
used as an `order statistic tree`_.  Rather than performing a linear scan,
values can be found in logarithmic time by repeatedly bisecting the internal
tree structure.  Methods for looking up values are
:func:`SortedList.__contains__`, :func:`SortedList.count`,
:func:`SortedList.index`, :func:`SortedList.bisect_left`,
:func:`SortedList.bisect_right`, and :func:`SortedList.__getitem__`.

    >>> sl = SortedList('abbcccddddeeeee')
    >>> 'f' in sl
    False
    >>> sl.count('e')
    5
    >>> sl.index('c')
    3
    >>> sl[3]
    'c'
    >>> sl.bisect_left('d')
    6
    >>> sl.bisect_right('d')
    10
    >>> sl[6:10]
    ['d', 'd', 'd', 'd']

Several methods can be used to iterate values in a :class:`SortedList`. There
are the typical sequence iterators: :func:`SortedList.__iter__` and
:func:`SortedList.__reversed__`. There are also methods for iterating by value
or by index using :func:`SortedList.irange` and
:func:`SortedList.islice`. These methods produce iterators that are faster than
repeatedly indexing the :class:`SortedList`.

    >>> sl = SortedList('acegi')
    >>> list(iter(sl))
    ['a', 'c', 'e', 'g', 'i']
    >>> list(reversed(sl))
    ['i', 'g', 'e', 'c', 'a']
    >>> list(sl.irange('b', 'h'))
    ['c', 'e', 'g']
    >>> list(sl.islice(1, 4))
    ['c', 'e', 'g']

A :class:`SortedList` also supports the typical sequence operators
:func:`SortedList.__add__` and :func:`SortedList.__mul__` as well as their
in-place counterparts.

    >>> sl = SortedList('abc')
    >>> sl + sl
    SortedList(['a', 'a', 'b', 'b', 'c', 'c'])
    >>> sl * 3
    SortedList(['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'])
    >>> sl += 'de'
    >>> sl
    SortedList(['a', 'b', 'c', 'd', 'e'])
    >>> sl *= 2
    >>> sl
    SortedList(['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd', 'e', 'e'])

Although :class:`SortedList` implements most of the mutable sequence methods,
there are five which are not implemented. Each of these methods assigns a value
at an index which is not supported by :class:`SortedList`.

    >>> sl = SortedList('abcde')
    >>> sl[2] = 'c'
    Traceback (most recent call last):
      ...
    NotImplementedError: use ``del sl[index]`` and ``sl.add(value)`` instead
    >>> sl.reverse()
    Traceback (most recent call last):
      ...
    NotImplementedError: use ``reversed(sl)`` instead
    >>> sl.append('f')
    Traceback (most recent call last):
      ...
    NotImplementedError: use ``sl.add(value)`` instead
    >>> sl.extend(['f', 'g', 'h'])
    Traceback (most recent call last):
      ...
    NotImplementedError: use ``sl.update(values)`` instead
    >>> sl.insert(5, 'f')
    Traceback (most recent call last):
      ...
    NotImplementedError: use ``sl.add(value)`` instead

Comparison with :class:`SortedList` uses lexicographical ordering as with other
sequence types.

Refer to the :doc:`Sorted List documentation<sortedlist>` for additional
parameters, more examples, and descriptions of runtime complexity.

.. _`order statistic tree`: https://en.wikipedia.org/wiki/Order_statistic_tree


Sorted-key List
---------------

The :doc:`Sorted Containers<index>` project also maintains a specialized
sorted-list-like type that accepts a key-parameter as found in Python's
built-in `sorted` function. :class:`SortedKeyList` provides the same
functionality as :class:`SortedList` but maintains the order of contained
values based on the applied key-function. This simplifies the pattern of boxing
and un-boxing which would otherwise be required.

    >>> from operator import neg
    >>> from sortedcontainers import SortedKeyList
    >>> skl = SortedKeyList(key=neg)

The key function extracts a comparison key for ordering items in the list. In
our example above we apply the negation operator. In the example above, a
sorted list of integers would be ordered in descending sort order.

You can also construct a :class:`SortedKeyList` using the :class:`SortedList`
type by passing a key-function to the initializer.

    >>> from sortedcontainers import SortedList
    >>> values = SortedList([1, 2, 3, 4, 5], key=neg)
    >>> values
    SortedKeyList([5, 4, 3, 2, 1], key=<built-in function neg>)
    >>> isinstance(values, SortedList)
    True
    >>> issubclass(SortedKeyList, SortedList)
    True
    >>> values.key
    <built-in function neg>

:class:`SortedKeyList` adds three additional methods to the :class:`SortedList`
type. They are :func:`SortedKeyList.bisect_key_left`,
:func:`SortedKeyList.bisect_key_right`, and :func:`SortedKeyList.irange_key`.
Each of these methods accepts the key rather than the value for its
:class:`SortedList` counterpart.

    >>> skl = SortedKeyList([1, 2, 3, 4, 5], key=neg)
    >>> skl
    SortedKeyList([5, 4, 3, 2, 1], key=<built-in function neg>)
    >>> skl.bisect_key_left(-4.5)
    1
    >>> skl.bisect_key_right(-1.5)
    4
    >>> list(skl.irange_key(-4.5, -1.5))
    [4, 3, 2]

Refer to the :doc:`Sorted List documentation<sortedlist>` for additional
parameters, more examples, and descriptions of runtime complexity.


Caveats
-------

:doc:`Sorted Containers<index>` data types have three requirements:

1. The comparison value or key must have a `total ordering`_.

2. The comparison value or key must not change while the value is stored in the
   sorted container.

3. If the key-function parameter is used, then equal values must have equal
   keys.

If any of these three requirements are violated then the warranty of
:doc:`Sorted Containers<index>` is void and it will not behave correctly. While
it may be possible to design useful data types that do not have these
requirements, these are the caveats of :doc:`Sorted Containers<index>` and they
match those of :doc:`alternative implementations<performance>`. Each of these
requirements allow for optimizations and together they are an attempt to find
the right tradeoff between functionality and performance.

Let's look at some examples of what works and what doesn't. In Python, all
objects inherit from ``object`` which provides a default implementation of
equality. In pseudocode, the object type looks something like:

    >>> class Object:
    ...     def __eq__(self, other):
    ...         return id(self) == id(other)

The default implementation defines equality in terms of identity. Note that
`Object` does not define comparison methods like less-than or
greater-than. While Python objects are comparable by default in Python 2, the
feature was removed in Python 3. Instances of `object` can *not* be stored in a
:class:`SortedList`.

We can extend this example by creating our own `Record` data type with `name`
and `rank` attributes.

    >>> class Record(object):
    ...     def __init__(self, name, rank):
    ...         self.name = name
    ...         self.rank = rank
    ...     def __eq__(self, other):
    ...         return self.name == other.name

The `Record` type defines equality in terms of its `name` attribute which may
be thought of as a record identifier. Each `Record` also has a `rank` which
would be useful for ranking records in sorted order. The `Record` type does not
define comparison operators and so can *not* be stored in a
:class:`SortedList`.

    >>> alice1 = Record('alice', 1)
    >>> bob2 = Record('bob', 2)
    >>> carol3 = Record('carol', 3)

Since the `rank` attribute is intended for ordering records, the key-function
presents a tempting but invalid use for ordering records::

    >>> get_rank = lambda record: record.rank
    >>> sl = SortedList([alice1, bob2, carol3], key=get_rank)

Although the sorted list now appears to work, the requirements have been
invalidated. Specifically #3, since it is now possible for equal values to have
inequal keys::

    >>> bob4 = Record('bob', 4)
    >>> bob2 == bob4  # Equal values.
    True
    >>> get_rank(bob2) == get_rank(bob4)
    False
    >>> # ^-- Equal values should have equal keys.
    >>> bob4 in sl  # <-- Here's the problem. BAD!
    False

In the example above, `bob4` can not be found in `sl` because although `bob2`
and `bob4` are equal, the corresponding keys are not equal. The mistake is a
bit easier to see without the key-function. The key-function defined
comparisons between records like so::

    >>> class Record(object):
    ...     def __init__(self, name, rank):
    ...         self.name = name
    ...         self.rank = rank
    ...     def __eq__(self, other):
    ...         return self.name == other.name
    ...     def __lt__(self, other):
    ...         return self.rank < other.rank

Written as above, equality between objects is more clearly seen as unrelated to
ordering between objects. This is the most common mistake made when using
:doc:`Sorted Containers<index>`. The `Record` type now also violates
requirement #1 because equal instances can also be strictly less than each
other::

    >>> bob2 = Record('bob', 2)
    >>> bob4 = Record('bob', 4)
    >>> bob2 == bob4
    True
    >>> bob2 < bob4  # <-- Here's the problem. BAD!
    True

In the above example, `bob2` and `bob4` are equal to each other while `bob2` is
also strictly less than `bob4`. The `Record` type therefore does not have a
`total ordering`_. In pseudocode the three requirements for a `total ordering`_
are:

I. If ``a <= b and b <= a`` then ``a == b``.

II. And if ``a <= b and b <= c`` then ``a <= c``.

III. And ``a <= b or b <= a``.

Intuitively, a `total ordering`_ is best understood through integer and string
types. Each of these common types defines a `total ordering`_ and can be used
for comparisons in :doc:`Sorted Containers<index>`. Of the built-in types in
Python, these have a `total ordering`_:

1. Integers

2. Strings and bytes.

3. All foating-point numbers except ``float('nan')``.

4. Sequences like `list` and `tuple` of values with a total ordering.

There are also some built-in Python types and values which lack a total
ordering:

1. Sets and frozensets (not a total ordering).

2. ``float('nan')`` (not a total ordering).

3. Mapping types (not comparable, changed in Python 3).

The best way to fix the `Record` type is to define equality and comparison in
terms of the same fields.

    >>> class Record(object):
    ...     def __init__(self, name, rank):
    ...         self.name = name
    ...         self.rank = rank
    ...     def _cmp_key(self):
    ...         return (self.rank, self.name)
    ...     def __eq__(self, other):
    ...         return self._cmp_key() == other._cmp_key()
    ...     def __lt__(self, other):
    ...         return self._cmp_key() < other._cmp_key()

The example above uses a comparison-key method named `_cmp_key` and the
lexicographical ordering semantics of tuples to define equality and comparison
in terms of the `rank` and `name` fields. It would also be possible to omit the
`Record.__lt__` method and instead use a key-function which called
`record._cmp_key()`. But the key-function will take more memory and be slower
as it uses a :class:`SortedKeyList` which stores a reference to the key for
every value.

The `Record` example above is complicated by equality defined as those objects
with equal names. When using equality inherited from `object`, that is, defined
in terms of instance identity, the situation is simplified. For example:

    >>> class Record(object):
    ...     def __init__(self, name, rank):
    ...         self.name = name
    ...         self.rank = rank
    ...     def __lt__(self, other):
    ...         return self.rank < other.rank

The `Record` type now can be stored in :class:`SortedList` because equality
based on instance identity guarantees the `rank` attributes are equal so long
as its value has a `total ordering`_.

    >>> alice1 = Record('alice', 1)
    >>> bob2 = Record('bob', 2)
    >>> carol3 = Record('carol', 3)
    >>> bob4 = Record('bob', 4)
    >>> bob2 != bob4  # <-- Different instances, so unequal. GOOD!
    True
    >>> sl = SortedList([alice1, bob2, carol3, bob4])
    >>> bob2 in sl
    True
    >>> bob4 in sl
    True

The above example displays that all three requirements are followed:

1. The comparison key, `rank`, is an integer, which has a `total ordering`_.

2. The comparison key does not change while the value is stored in the sorted
   container.

3. Equal `Record` instances have equal `rank` attributes based on instance
   identity.

These examples can be summarized in two pieces of advice:

1. If the data type defines its own equality, that is ``__eq__``, then make
   sure the comparison methods or key-function define a `total ordering`_ and
   equal values have equal comparison keys.

2. If the data type does not define equality then it inherits equality from
   `object` and uses instance identity. Compare objects using comparison
   methods like ``__lt__`` or the key-function. The compared values must have a
   `total ordering`_.

Another invalid use case of :class:`SortedKeyList` occurs when the key-function
returns a different comparison key for a given value while the value is stored
in the sorted container.

    >>> from random import random
    >>> key_func = lambda value: random()
    >>> sl = SortedList([1, 2, 3, 4, 5], key=key_func)
    >>> # ^-- Corrupt sorted list.
    >>> 3 in sl
    False
    >>> key_func(1) == key_func(1)  # <-- Here's the problem. BAD!
    False

The example above violates two requirements of sorted lists: equal values must
have equal keys and the key function must return the same key for the given
value while the value is stored in the sorted container. The `random`
key-function does not reliably return the same key for a given value. The order
of values in a sorted container can be made arbitrary and reliable by changing
the key-function like so:

    >>> from random import seed
    >>> def key_func(value):
    ...     "Key-function for arbitrary but reliable order."
    ...     seed(value)
    ...     return random()

Another way the problem above manifests itself is when the comparison key of an
object is mutated while the object is stored in the :class:`SortedList`. Using
the `Record` definition from above:

    >>> class Record(object):
    ...     def __init__(self, name, rank):
    ...         self.name = name
    ...         self.rank = rank
    ...     def __lt__(self, other):
    ...         return self.rank < other.rank
    >>> alice1 = Record('alice', 1)
    >>> bob2 = Record('bob', 2)
    >>> carol3 = Record('carol', 3)
    >>> sl = SortedList([alice1, bob2, carol3])
    >>> bob2 in sl
    True

Python objects are typically mutable so while the above example works and is
correct, there's nothing preventing a modification to the `rank` of a `Record`.
If the `rank` is modified while the `Record` instance is stored in the
:class:`SortedList`, then the container is corrupted.

    >>> bob2.rank = 20  # <-- Here's the problem. BAD!
    >>> bob2 in sl
    False

The `Record` instance `bob2` can no longer be found in the :class:`SortedList`
because modifying the `rank` changed its sort order position without updating
its position in `sl`. To modify the sorted order position, :func:`remove
<SortedList.remove>` the value, update it, and then :func:`add
<SortedList.add>` the value back again.

Similar limitations also apply to Python's `dict` data type which can be
corrupted by modifying the hash of a key while the item is stored in the
`dict`. The hashing protocol also requires that equal keys have equal hashes.

One final caveat: indexing a sorted list is fast but not as fast as indexing
Python's built-in list data type. The runtime complexity for indexing a sorted
list is `O(log(n))` while it is `O(1)` for Python's built-in list data type.
Indexing a sorted list requires building and maintaining a positional index
which is not built if not necessary. The index is fast and light on memory
overhead but avoid positional indexing if able. Indexing at the front or back,
indexes like `0` and `-1`, is optimized and will not require the positional
index.

.. _`total ordering`: https://en.wikipedia.org/wiki/Total_order


Sorted Dict
-----------

Built atop Python's built-in `dict` data type and :class:`SortedList` is the
mutable mapping data type :class:`SortedDict`. Sorted dict keys are maintained
in sorted order. The design of :class:`SortedDict` is simple: sorted dict
inherits from `dict` to store items and maintains a sorted list of
keys. :class:`SortedDict` keys must be hashable and comparable. The hash and
total ordering of keys must not change while they are stored in the
:class:`SortedDict`.

    >>> from sortedcontainers import SortedDict
    >>> sd = SortedDict()

Items may be added to a :class:`SortedDict` using
:func:`SortedDict.__setitem__`, :func:`SortedDict.update` or
:func:`SortedDict.setdefault`. When doing so, the keys remain sorted.

    >>> sd['e'] = 5
    >>> sd['b'] = 2
    >>> sd
    SortedDict({'b': 2, 'e': 5})
    >>> sd.update({'d': 4, 'c': 3})
    >>> sd
    SortedDict({'b': 2, 'c': 3, 'd': 4, 'e': 5})
    >>> sd.setdefault('a', 1)
    1
    >>> sd
    SortedDict({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})

Several methods may be used to remove items by key or by index. The methods
:func:`SortedDict.__delitem__` and :func:`SortedDict.pop` remove items by
key. And the method :func:`SortedDict.popitem` removes items by index.

    >>> del sd['d']
    >>> sd.pop('c')
    3
    >>> sd.popitem(index=-1)
    ('e', 5)
    >>> sd
    SortedDict({'a': 1, 'b': 2})

Because :class:`SortedDict` uses both `dict` and :class:`SortedList`, there are
many methods for looking up keys from each type. The mapping interface supports
:func:`SortedDict.__getitem__`, :func:`SortedDict.__contains__`,
:func:`SortedDict.get`, and :func:`SortedDict.peekitem`.

    >>> sd['b']
    2
    >>> 'c' in sd
    False
    >>> sd.get('z') is None
    True
    >>> sd.peekitem(index=-1)
    ('b', 2)

The sequence interface supports the same lookup methods as those provided by
:class:`SortedList`.

    >>> sd.bisect_right('b')
    2
    >>> sd.index('a')
    0
    >>> list(sd.irange('a', 'z'))
    ['a', 'b']

The keys, items, and values views also support both set semantics and sequence
semantics with optimized methods for lookups by index.

    >>> keys = sd.keys()
    >>> keys[0]
    'a'
    >>> items = sd.items()
    >>> items[-1]
    ('b', 2)
    >>> values = sd.values()
    >>> values[:]
    [1, 2]

The :class:`SortedDict` initializer supports one additional position argument.
The positional argument must come before any sequences, mappings, or keyword
arguments used to initialize the items in a :class:`SortedDict`. The first
positional argument is an optional callable key-function used to extract a
comparison key from the keys of the :class:`SortedDict`. For example, to
construct a :class:`SortedDict` with integer keys in descending order:

    >>> sd = SortedDict(neg, enumerate('abc', start=1))
    >>> sd
    SortedDict(<built-in function neg>, {3: 'c', 2: 'b', 1: 'a'})
    >>> keys = sd.keys()
    >>> list(keys)
    [3, 2, 1]

Because :class:`SortedDict` inherits from `dict`, the `__missing__` method can
be used to give missing keys a default value. Customizing the `__missing__`
method creates a kind of `defaultdict` like that in the `collections` module.

    >>> class DefaultSortedDict(SortedDict):
    ...     def __missing__(self, key):
    ...         return 0
    >>> dsd = DefaultSortedDict()
    >>> dsd['z']
    0

Refer to the :doc:`Sorted Dict documentation<sorteddict>` for additional
parameters, more examples, and descriptions of runtime complexity.


Sorted Set
----------

Standing on the shoulder's of Python's built-in `set` data type and
:class:`SortedList` is the mutable set data type :class:`SortedSet`. Sorted set
values are maintained in sorted order. The design of :class:`SortedSet` is
simple: sorted set uses Python's built-in `set` for set-operations and
maintains a sorted list of values. Values stored in a :class:`SortedSet` must
be hashable and comparable.  The hash and total ordering of values must not
change while they are stored in the :class:`SortedSet`.

    >>> from sortedcontainers import SortedSet
    >>> ss = SortedSet()

:class:`SortedSet` implements optimized versions of the core mutable set
methods: :func:`SortedSet.__contains__`, :func:`SortedSet.add`,
:func:`SortedSet.update`, :func:`SortedSet.discard`, and the more strict
:func:`SortedSet.remove`.

    >>> ss.add('c')
    >>> ss.add('a')
    >>> ss.add('b')
    >>> ss
    SortedSet(['a', 'b', 'c'])
    >>> 'c' in ss
    True
    >>> ss.discard('a')
    >>> ss.remove('b')
    >>> _ = ss.update('def')
    >>> ss
    SortedSet(['c', 'd', 'e', 'f'])

:class:`SortedSet` also behaves like a sequence with
:func:`SortedSet.__getitem__` and :func:`SortedSet.__reversed__` methods. And
includes the mutable sequence methods :func:`SortedSet.__delitem__` and
:func:`SortedSet.pop`.

    >>> ss[0]
    'c'
    >>> list(reversed(ss))
    ['f', 'e', 'd', 'c']
    >>> del ss[0]
    >>> ss.pop(index=-1)
    'f'
    >>> ss
    SortedSet(['d', 'e'])

Set-operation methods like :func:`SortedSet.difference`,
:func:`SortedSet.intersection`, :func:`SortedSet.symmetric_difference`, and
:func:`SortedSet.union`, as well as their in-place counterparts and operators
are all supported.

    >>> abcd = SortedSet('abcd')
    >>> cdef = SortedSet('cdef')
    >>> abcd.difference(cdef)
    SortedSet(['a', 'b'])
    >>> abcd.intersection(cdef)
    SortedSet(['c', 'd'])
    >>> abcd.symmetric_difference(cdef)
    SortedSet(['a', 'b', 'e', 'f'])
    >>> abcd.union(cdef)
    SortedSet(['a', 'b', 'c', 'd', 'e', 'f'])
    >>> abcd | cdef
    SortedSet(['a', 'b', 'c', 'd', 'e', 'f'])
    >>> abcd |= cdef
    >>> abcd
    SortedSet(['a', 'b', 'c', 'd', 'e', 'f'])

Several :class:`SortedList` methods are also exposed on :class:`SortedSet`
objects like :func:`SortedList.bisect`, :func:`SortedList.index`,
:func:`SortedList.irange`, and :func:`SortedList.islice` just as with
:class:`SortedDict`.

    >>> ss = SortedSet('abcdef')
    >>> ss.bisect('d')
    4
    >>> ss.index('f')
    5
    >>> list(ss.irange('b', 'e'))
    ['b', 'c', 'd', 'e']
    >>> list(ss.islice(-3))
    ['d', 'e', 'f']

Like :class:`SortedList` an additional `key` parameter can be used to
initialize the :class:`SortedSet` with a callable which is used to extract a
comparison key.

    >>> ss = SortedSet([1, 2, 3], key=neg)
    >>> ss
    SortedSet([3, 2, 1], key=<built-in function neg>)

Sorted set comparisons use subset and superset relations. Two sorted sets are
equal if and only if every element of each sorted set is contained in the other
(each is a subset of the other). A sorted set is less than another sorted set
if and only if the first sorted set is a proper subset of the second sorted set
(is a subset, but is not equal). A sorted set is greater than another sorted
set if and only if the first sorted set is a proper superset of the second
sorted set (is a superset, but is not equal). The comparison semantics of
sorted sets do not define a total ordering.

Refer to the :doc:`Sorted Set documentation<sortedset>` for additional
parameters, more examples, and descriptions of runtime complexity.


Migrating
---------

The :doc:`performance comparison<performance>` page documents several
alternative implementations of the sorted types described. Some of those
projects have deprecated themselves and now recommend :doc:`Sorted
Containers<index>` instead. When migrating from other projects, there are a
couple of things to keep in mind.

:doc:`Sorted Containers<index>` went through a major version change between
version one and version two. The goal of the change was to adopt Python 3
semantics wherever possible:

1. Several :class:`SortedList` methods now raise :exc:`NotImplementedError`:
   :func:`SortedList.__setitem__`, :func:`SortedList.append`, and
   :func:`SortedList.extend`. Use :func:`SortedList.add` or
   :func:`SortedList.update` instead.

2. :class:`SortedDict` has adopted the Python 3 semantics of `dict` views as
   the default. The :func:`SortedDict.keys`, :func:`SortedDict.items`, and
   :func:`SortedDict.values` methods now return views with support for
   optimized indexing. The view objects also implement set and sequence
   protocol methods. Prefer using the :class:`SortedDict` methods directly for
   better performance.

3. Some type and parameter names were changed. `SortedListWithKey` was renamed
   to `SortedKeyList` but an alias remains for compatibility. Several methods
   which accepted a `val` parameter now accept `value` for better readability.

The :doc:`history` documents all the changes made in every version in the
history of the project. The :ref:`Version 2<v2>` release notes detail all the
changes made.

The `blist`_ project remains the most similar as its API was the original
inspiration for :doc:`Sorted Containers<index>`. The main difference has always
been the :func:`SortedList.pop` method. The `blist`_ project pops the first
element by default while :doc:`Sorted Containers<index>` pops the last element
and matches the API of Python's built-in `list` data type. The sorted dict data
type in `blist`_ also continues to use the old Python 2 semantics for `dict`
views.

The `bintrees`_ project now recommends using :doc:`Sorted Containers<index>`
instead and has stopped development. The API differs significantly but the
supported functionality is the same. The `Tree` object in `bintrees`_ is most
similar to :class:`SortedDict`. All of the mapping methods and set methods are
available using either :class:`SortedDict` or :class:`SortedKeysView`. The
slicing methods and previous/successor iterator methods correspond to
:func:`SortedDict.irange` and the heap methods correspond to indexing with
views like :func:`SortedKeysView.__getitem__`.

The `banyan`_ project has data types similar to :class:`SortedDict` and
:class:`SortedSet`. Most methods have a direct counterpart in :doc:`Sorted
Containers<index>`. But the frozen sorted dict and frozen sorted set data types
have no direct comparison. The functionality of hashing can be implemented by
inheriting and defining the `__hash__` method. Do so with care, because the
instance is still mutable. The `banyan`_ project also supports tree
augmentation which can be useful in implementing interval trees or segment
trees. There is no support for tree argumentation in :doc:`Sorted
Containers<index>`.

.. _`blist`: https://pypi.org/project/blist/
.. _`bintrees`: https://pypi.org/project/bintrees/
.. _`banyan`: https://pypi.org/project/Banyan/
