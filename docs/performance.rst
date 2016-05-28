Performance Comparison
======================

Measuring performance is a difficult task. All the benchmarks on this page are
synthetic in the sense that they test one function repeatedly. Measurements in
live systems are much harder to produce reliably. So take the following data
with a grain of salt. That being said, a stated feature of
:doc:`SortedContainers<index>` is performance so we would be remiss not to
produce this page with comparisons.

The source for all benchmarks can be found under the "tests" directory in the
files prefixed "benchmark." Measurements are made from the min, max, and mean
of 5 repetitions. In the graphs below, the line follows the mean and at each
point, the min/max displays the bounds. Note that the axes are log-log so
properly reading two different lines would describe one metric as "X times"
faster rather than "X seconds" faster. In all graphs, lower is
better. Measurements are made by powers of ten: 100 through 1,000,000.

Measurements up to 10,000,000,000 elements have been successfully tested and
benchmarks. Read :doc:`Performance at Scale<performance-scale>` for
details. Only a couple implementations (including SortedContainers) are capable
of handling so many elements. The major limiting factor at that size is
memory. Consider the simple case of storing CPython's integers in a
SortedList. Each integer object requires ~24 bytes so one hundred million
elements will require about three gigabytes of memory. If the implemenation
adds significant overhead then most systems will run out of memory. For all
datasets which may be kept in memory, :doc:`SortedContainers<index>` is an
excellent choice.

A good effort has been made to find competing implementations. Six in total
were found with various list, set, and dict implementations.

rbtree
  Provides a fast, C-implementation for dict and set data types.
  `rbtree on PyPI <https://pypi.python.org/pypi/rbtree>`_

blist
  Provides list, dict, and set containers based on the blist data-type.
  Implemented in Python and C.
  `blist on PyPI <https://pypi.python.org/pypi/blist>`_

treap
  Uses Cython for improved performance and provides a dict container.
  `treap on PyPI <https://pypi.python.org/pypi/treap>`_

bintrees
  Provides several tree-based implementations for dict and set containers.
  Fastest were AVL and Red-Black trees. Extends the conventional API to
  provide set operations for the dict type. Implemented in C.
  `bintrees on PyPI <https://pypi.python.org/pypi/bintrees>`_

banyan
  Provides a fast, C-implementation for dict and set data types. Offers some
  features also found in sortedcontainers like accessing the n-th item in a
  set or dict.
  `banyan on PyPI <https://pypi.python.org/pypi/Banyan>`_

skiplistcollections
  Pure-Python implementation based on skip-lists providing a limited API
  for dict and set types.
  `skiplistcollections on PyPI <https://pypi.python.org/pypi/skiplistcollections>`_

sortedcollection
  Pure-Python implementation of sorted list based solely on a list.
  Feature-poor and inefficient for writes but included because it is written
  by Raymond Hettinger and linked from the official Python docs.
  `sortedcollection on ActiveState <http://code.activestate.com/recipes/577197-sortedcollection/>`_

Several competing implementations were omitted because they were not easily
installable or failed to build.

ruamel.ordereddict.sorteddict
  C-implementation that only supports Python 2. Performance was measured in
  correspondence with the module author. Performance was generally very good
  except for ``__delitem__``. At scale, deleting entries became exceedingly
  slow.
  `ruamel.ordereddict on PyPI <https://pypi.python.org/pypi/ruamel.ordereddict/>`_

rbtree from NewCenturyComputers
  Pure-Python tree-based implementation. Not sure when this was last updated.
  Unlikely to be fast.
  `rbtree from NewCenturyComputers <http://newcenturycomputers.net/projects/rbtree.html>`_

python-avl-tree from Github user pgrafov
  Pure-Python tree-based implementation. Last updated in 2010. Unlikely
  to be fast.
  `python-avl-tree from Github user pgrafov <https://github.com/pgrafov/python-avl-tree>`_

pyavl
  C-implementation for AVL tree-based dict and set containers. Claims to be
  fast. Lacking documentation and failed to build.
  `pyavl on PyPI <https://pypi.python.org/pypi/pyavl>`_

The most similar module to :doc:`SortedContainers<index>` is
skiplistcollections given that each is implemented in Python. But as is
displayed below, :doc:`SortedContainers<index>` is several times faster and
provides a richer API. Often the pure-Python implementation in SortedContainers
is faster even than the C-implementation counterparts. Where it lacks,
performance is generally on the same magnitude.

Because :doc:`SortedContainers<index>` is implemented in pure-Python, its
performance depends directly on the Python runtime. A :doc:`runtime performance
comparison<performance-runtime>` is also included with data from popular
runtimes.

:doc:`SortedContainers<index>` uses a segmented-list data structure similar to
a B-tree limited to two levels of nodes. As part of the implementation, a load
factor is used to determine how many values should be stored in each node. This
can have a significant impact on performance and a :doc:`load factor
performance comparison<performance-load>` is also provided.

Though these benchmarks exercise only one API repeatedly, an effort has also
been made to simulate real-world workloads. The :doc:`simulated workload
performance comparison<performance-workload>` contains examples with
comparisons to other implementations, load factors, and runtimes.

A couple final notes about the graphs below. Missing data indicates the
benchmark either took too long or failed. The set operations with tiny, small,
medium, and large variations indicate the size of the container involved in the
right-hand-side of the operation: tiny is exactly 10 elements; small is 10% of
the size of the left-hand-side; medium is 50%; and large is 100%. The
sortedcontainers module uses a different algorithm based on the size of the
right-hand-side of the operation for a dramatic improvement in performance.

SortedList
----------

Graphs comparing :doc:`SortedList<sortedlist>` performance.

__init__
........

Initializing with a list of random numbers.

.. image:: _static/SortedList-init.png

add
...

Randomly adding values using :ref:`SortedList.add<SortedList.add>`.

.. image:: _static/SortedList-add.png

contains
........

Randomly testing membership using
:ref:`SortedList.__contains__<SortedList.__contains__>`.

.. image:: _static/SortedList-contains.png

count
.....

Counting objects at random using :ref:`SortedList.count<SortedList.count>`.

.. image:: _static/SortedList-count.png

__delitem__
...........

Deleting objects at random using
:ref:`SortedList.__delitem__<SortedList.__delitem__>`.

.. image:: _static/SortedList-delitem.png

__getitem__
...........

Retrieving ojbects by index using
:ref:`SortedList.__getitem__<SortedList.__getitem__>`.

.. image:: _static/SortedList-getitem.png

index
.....

Finding the index of an object using :ref:`SortedList.index<SortedList.index>`.

.. image:: _static/SortedList-index.png

iter
....

Iterating a SortedList using :ref:`SortedList.__iter__<SortedList.__iter__>`.

.. image:: _static/SortedList-iter.png

pop
...

Removing the last object using :ref:`SortedList.pop<SortedList.pop>`.

.. image:: _static/SortedList-pop.png

remove
......

Remove an object at random using :ref:`SortedList.remove<SortedList.remove>`.

.. image:: _static/SortedList-remove.png

update_large
............

Updating a SortedList with a large iterable using
:ref:`SortedList.update<SortedList.update>`.

.. image:: _static/SortedList-update_large.png

update_small
............

Updating a SortedList with a small iterable using
:ref:`SortedList.update<SortedList.update>`.

.. image:: _static/SortedList-update_small.png

SortedDict
----------

Graphs comparing :doc:`SortedDict<sorteddict>` performance.

__init__
........

Initializing with a list of pairs of random numbers.

.. image:: _static/SortedDict-init.png

__contains__
............

Given a key at random, test whether the key is in the dictionary using
:ref:`SortedDict.__contains__<SortedDict.__contains__>`.

.. image:: _static/SortedDict-contains.png

__getitem__
...........

Given a key at random, retrieve the value using
:ref:`SortedDict.__getitem__<SortedDict.__getitem__>`.

.. image:: _static/SortedDict-getitem.png

__setitem__
...........

Given a key at random, set the value using
:ref:`SortedDict.__setitem__<SortedDict.__setitem__>`.

.. image:: _static/SortedDict-setitem.png

__delitem__
...........

Given a key at random, delete the value using
:ref:`SortedDict.__delitem__<SortedDict.__delitem__>`.

.. image:: _static/SortedDict-delitem.png

iter
....

Iterate the keys of a SortedDict using
:ref:`SortedDict.__iter__<SortedDict.__iter__>`.

.. image:: _static/SortedDict-iter.png

setitem_existing
................

Given an existing key at random, set the value using
:ref:`SortedDict.__setitem__<SortedDict.__setitem__>`.

.. image:: _static/SortedDict-setitem_existing.png

SortedSet
---------

Graphs comparing :doc:`SortedSet<sortedset>` performance.

__init__
........

Initializing with a list of random numbers.

.. image:: _static/SortedSet-init.png

add
...

Randomly add values using :ref:`SortedSet.add<SortedSet.add>`.

.. image:: _static/SortedSet-add.png

contains
........

Randomly test membership using
:ref:`SortedSet.__contains__<SortedSet.__contains__>`.

.. image:: _static/SortedSet-contains.png

difference_large
................

Set difference using :ref:`SortedSet.difference<SortedSet.difference>`.

.. image:: _static/SortedSet-difference_large.png

difference_medium
.................

Set difference using :ref:`SortedSet.difference<SortedSet.difference>`.

.. image:: _static/SortedSet-difference_medium.png

difference_small
................

Set difference using :ref:`SortedSet.difference<SortedSet.difference>`.

.. image:: _static/SortedSet-difference_small.png

difference_tiny
...............

Set difference using :ref:`SortedSet.difference<SortedSet.difference>`.

.. image:: _static/SortedSet-difference_tiny.png

difference_update_large
.......................

Set difference using
:ref:`SortedSet.difference_update<SortedSet.difference_update>`.

.. image:: _static/SortedSet-difference_update_large.png

difference_update_medium
........................

Set difference using
:ref:`SortedSet.difference_update<SortedSet.difference_update>`.

.. image:: _static/SortedSet-difference_update_medium.png

difference_update_small
.......................

Set difference using
:ref:`SortedSet.difference_update<SortedSet.difference_update>`.

.. image:: _static/SortedSet-difference_update_small.png

difference_update_tiny
......................

Set difference using
:ref:`SortedSet.difference_update<SortedSet.difference_update>`.

.. image:: _static/SortedSet-difference_update_tiny.png

intersection_large
..................

Set intersection using :ref:`SortedSet.intersection<SortedSet.intersection>`.

.. image:: _static/SortedSet-intersection_large.png

intersection_medium
...................

Set intersection using :ref:`SortedSet.intersection<SortedSet.intersection>`.

.. image:: _static/SortedSet-intersection_medium.png

intersection_small
..................

Set intersection using :ref:`SortedSet.intersection<SortedSet.intersection>`.

.. image:: _static/SortedSet-intersection_small.png

intersection_tiny
.................

Set intersection using :ref:`SortedSet.intersection<SortedSet.intersection>`.

.. image:: _static/SortedSet-intersection_tiny.png

intersection_update_large
.........................

Set intersection using
:ref:`SortedSet.intersection_update<SortedSet.intersection_update>`.

.. image:: _static/SortedSet-intersection_update_large.png

intersection_update_medium
..........................

Set intersection using
:ref:`SortedSet.intersection_update<SortedSet.intersection_update>`.

.. image:: _static/SortedSet-intersection_update_medium.png

intersection_update_small
.........................

Set intersection using
:ref:`SortedSet.intersection_update<SortedSet.intersection_update>`.

.. image:: _static/SortedSet-intersection_update_small.png

intersection_update_tiny
........................

Set intersection using
:ref:`SortedSet.intersection_update<SortedSet.intersection_update>`.

.. image:: _static/SortedSet-intersection_update_tiny.png

iter
....

Iterating a set using :ref:`iter(SortedSet)<SortedSet.__iter__>`.

.. image:: _static/SortedSet-iter.png

pop
...

Remove the last item in a set using :ref:`SortedSet.pop<SortedSet.pop>`.

.. image:: _static/SortedSet-pop.png

remove
......

Remove an item at random using :ref:`SortedSet.remove<SortedSet.remove>`.

.. image:: _static/SortedSet-remove.png

union_large
...........

Set union using :ref:`SortedSet.union<SortedSet.union>`.

.. image:: _static/SortedSet-union_large.png

union_medium
............

Set union using :ref:`SortedSet.union<SortedSet.union>`.

.. image:: _static/SortedSet-union_medium.png

union_small
...........

Set union using :ref:`SortedSet.union<SortedSet.union>`.

.. image:: _static/SortedSet-union_small.png

union_tiny
..........

Set union using :ref:`SortedSet.union<SortedSet.union>`.

.. image:: _static/SortedSet-union_tiny.png

update_large
............

Set update using :ref:`SortedSet.update<SortedSet.update>`.

.. image:: _static/SortedSet-update_large.png

update_medium
.............

Set update using :ref:`SortedSet.update<SortedSet.update>`.

.. image:: _static/SortedSet-update_medium.png

update_small
............

Set update using :ref:`SortedSet.update<SortedSet.update>`.

.. image:: _static/SortedSet-update_small.png

update_tiny
...........

Set update using :ref:`SortedSet.update<SortedSet.update>`.

.. image:: _static/SortedSet-update_tiny.png

symmetric_difference_large
..........................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference<SortedSet.symmetric_difference>`.

.. image:: _static/SortedSet-symmetric_difference_large.png

symmetric_difference_medium
...........................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference<SortedSet.symmetric_difference>`.

.. image:: _static/SortedSet-symmetric_difference_medium.png

symmetric_difference_small
..........................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference<SortedSet.symmetric_difference>`.

.. image:: _static/SortedSet-symmetric_difference_small.png

symmetric_difference_tiny
.........................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference<SortedSet.symmetric_difference>`.

.. image:: _static/SortedSet-symmetric_difference_tiny.png

symm_diff_update_large
......................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference_update<SortedSet.symmetric_difference_update>`.

.. image:: _static/SortedSet-symmetric_difference_update_large.png

symm_diff_update_medium
.......................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference_update<SortedSet.symmetric_difference_update>`.

.. image:: _static/SortedSet-symmetric_difference_update_medium.png

symm_diff_update_small
......................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference_update<SortedSet.symmetric_difference_update>`.

.. image:: _static/SortedSet-symmetric_difference_update_small.png

symm_diff_update_tiny
.....................

Set symmetric-difference using
:ref:`SortedSet.symmetric_difference_update<SortedSet.symmetric_difference_update>`.

.. image:: _static/SortedSet-symmetric_difference_update_tiny.png
