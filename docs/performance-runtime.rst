Runtime Performance Comparison
==============================

Because :doc:`Sorted Containers<index>` is implemented in pure-Python, its
performance depends directly on the Python runtime. :doc:`Sorted
Containers<index>` is primarily developed, tested and benchmarked on CPython
3.6.

Not all runtimes are created equal. The graphs below compare :doc:`Sorted
Containers<index>` running on the CPython 3.6, CPython 2.7, and PyPy
runtimes. As of Python 3.6 the CPython 3.6 runtime is now faster than the
CPython 2.7 runtime. The PyPy runtime displays much more variability due to its
JIT-ed nature. Once the just-in-time compiler optimizes the code, performance
is often two to ten times faster.

Performance of competing implementations are benchmarked against the CPython
3.6 runtime. An :doc:`implementation performance comparison<performance>` is
also included with data from popular sorted container packages.

:doc:`Sorted Containers<index>` uses a segmented-list data structure similar to
a B-tree limited to two levels of nodes. As part of the implementation, a load
factor is used to determine how many values should be stored in each node. This
can have a significant impact on performance and a :doc:`load factor
performance comparison<performance-load>` is also provided.

Though these benchmarks exercise only one API repeatedly, an effort has also
been made to simulate real-world workloads. The :doc:`simulated workload
performance comparison<performance-workload>` contains examples with
comparisons to other implementations, load factors, and runtimes.

.. currentmodule:: sortedcontainers

Sorted List
-----------

Graphs comparing :doc:`sortedlist` performance.

__init__
........

Initializing with a list of random numbers using :func:`SortedList.__init__`.

.. image:: _static/SortedList_runtime-init.png

add
...

Randomly adding values using :func:`SortedList.add`.

.. image:: _static/SortedList_runtime-add.png

contains
........

Randomly testing membership using :func:`SortedList.__contains__`.

.. image:: _static/SortedList_runtime-contains.png

count
.....

Counting objects at random using :func:`SortedList.count`.

.. image:: _static/SortedList_runtime-count.png

__delitem__
...........

Deleting objects at random using :func:`SortedList.__delitem__`.

.. image:: _static/SortedList_runtime-delitem.png

__getitem__
...........

Retrieving ojbects by index using :func:`SortedList.__getitem__`.

.. image:: _static/SortedList_runtime-getitem.png

index
.....

Finding the index of an object using :func:`SortedList.index`.

.. image:: _static/SortedList_runtime-index.png

iter
....

Iterating a SortedList using :func:`SortedList.__iter__`.

.. image:: _static/SortedList_runtime-iter.png

pop
...

Removing the last object using :func:`SortedList.pop`.

.. image:: _static/SortedList_runtime-pop.png

remove
......

Remove an object at random using :func:`SortedList.remove`.

.. image:: _static/SortedList_runtime-remove.png

update_large
............

Updating a SortedList with a large iterable using :func:`SortedList.update`.

.. image:: _static/SortedList_runtime-update_large.png

update_small
............

Updating a SortedList with a small iterable using :func:`SortedList.update`.

.. image:: _static/SortedList_runtime-update_small.png

Sorted Dict
-----------

Graphs comparing :doc:`sorteddict` performance.

__init__
........

Initializing with a list of pairs of random numbers using
:func:`SortedDict.__init__`.

.. image:: _static/SortedDict_runtime-init.png

__contains__
............

Given a key at random, test whether the key is in the dictionary using
:func:`SortedDict.__contains__`.

.. image:: _static/SortedDict_runtime-contains.png

__getitem__
...........

Given a key at random, retrieve the value using :func:`SortedDict.__getitem__`.

.. image:: _static/SortedDict_runtime-getitem.png

__setitem__
...........

Given a key at random, set the value using :func:`SortedDict.__setitem__`.

.. image:: _static/SortedDict_runtime-setitem.png

__delitem__
...........

Given a key at random, delete the value using :func:`SortedDict.__delitem__`.

.. image:: _static/SortedDict_runtime-delitem.png

iter
....

Iterate the keys of a SortedDict using :func:`SortedDict.__iter__`.

.. image:: _static/SortedDict_runtime-iter.png

setitem_existing
................

Given an existing key at random, set the value using
:func:`SortedDict.__setitem__`.

.. image:: _static/SortedDict_runtime-setitem_existing.png

Sorted Set
----------

Graphs comparing :doc:`sortedset` performance.

__init__
........

Initializing with a list of random numbers using :func:`SortedSet.__init__`.

.. image:: _static/SortedSet_runtime-init.png

add
...

Randomly add values using :func:`SortedSet.add`.

.. image:: _static/SortedSet_runtime-add.png

contains
........

Randomly test membership using :func:`SortedSet.__contains__`.

.. image:: _static/SortedSet_runtime-contains.png

difference_large
................

Set difference using :func:`SortedSet.difference`.

.. image:: _static/SortedSet_runtime-difference_large.png

difference_medium
.................

Set difference using :func:`SortedSet.difference`.

.. image:: _static/SortedSet_runtime-difference_medium.png

difference_small
................

Set difference using :func:`SortedSet.difference`.

.. image:: _static/SortedSet_runtime-difference_small.png

difference_tiny
...............

Set difference using :func:`SortedSet.difference`.

.. image:: _static/SortedSet_runtime-difference_tiny.png

difference_update_large
.......................

Set difference using :func:`SortedSet.difference_update`.

.. image:: _static/SortedSet_runtime-difference_update_large.png

difference_update_medium
........................

Set difference using :func:`SortedSet.difference_update`.

.. image:: _static/SortedSet_runtime-difference_update_medium.png

difference_update_small
.......................

Set difference using :func:`SortedSet.difference_update`.

.. image:: _static/SortedSet_runtime-difference_update_small.png

difference_update_tiny
......................

Set difference using :func:`SortedSet.difference_update`.

.. image:: _static/SortedSet_runtime-difference_update_tiny.png

intersection_large
..................

Set intersection using :func:`SortedSet.intersection`.

.. image:: _static/SortedSet_runtime-intersection_large.png

intersection_medium
...................

Set intersection using :func:`SortedSet.intersection`.

.. image:: _static/SortedSet_runtime-intersection_medium.png

intersection_small
..................

Set intersection using :func:`SortedSet.intersection`.

.. image:: _static/SortedSet_runtime-intersection_small.png

intersection_tiny
.................

Set intersection using :func:`SortedSet.intersection`.

.. image:: _static/SortedSet_runtime-intersection_tiny.png

intersection_update_large
.........................

Set intersection using :func:`SortedSet.intersection_update`.

.. image:: _static/SortedSet_runtime-intersection_update_large.png

intersection_update_medium
..........................

Set intersection using :func:`SortedSet.intersection_update`.

.. image:: _static/SortedSet_runtime-intersection_update_medium.png

intersection_update_small
.........................

Set intersection using :func:`SortedSet.intersection_update`.

.. image:: _static/SortedSet_runtime-intersection_update_small.png

intersection_update_tiny
........................

Set intersection using :func:`SortedSet.intersection_update`.

.. image:: _static/SortedSet_runtime-intersection_update_tiny.png

iter
....

Iterating a set using :func:`iter(SortedSet)`.

.. image:: _static/SortedSet_runtime-iter.png

pop
...

Remove the last item in a set using :func:`SortedSet.pop`.

.. image:: _static/SortedSet_runtime-pop.png

remove
......

Remove an item at random using :func:`SortedSet.remove`.

.. image:: _static/SortedSet_runtime-remove.png

union_large
...........

Set union using :func:`SortedSet.union`.

.. image:: _static/SortedSet_runtime-union_large.png

union_medium
............

Set union using :func:`SortedSet.union`.

.. image:: _static/SortedSet_runtime-union_medium.png

union_small
...........

Set union using :func:`SortedSet.union`.

.. image:: _static/SortedSet_runtime-union_small.png

union_tiny
..........

Set union using :func:`SortedSet.union`.

.. image:: _static/SortedSet_runtime-union_tiny.png

update_large
............

Set update using :func:`SortedSet.update`.

.. image:: _static/SortedSet_runtime-update_large.png

update_medium
.............

Set update using :func:`SortedSet.update`.

.. image:: _static/SortedSet_runtime-update_medium.png

update_small
............

Set update using :func:`SortedSet.update`.

.. image:: _static/SortedSet_runtime-update_small.png

update_tiny
...........

Set update using :func:`SortedSet.update`.

.. image:: _static/SortedSet_runtime-update_tiny.png

symmetric_difference_large
..........................

Set symmetric-difference using :func:`SortedSet.symmetric_difference`.

.. image:: _static/SortedSet_runtime-symmetric_difference_large.png

symmetric_difference_medium
...........................

Set symmetric-difference using :func:`SortedSet.symmetric_difference`.

.. image:: _static/SortedSet_runtime-symmetric_difference_medium.png

symmetric_difference_small
..........................

Set symmetric-difference using :func:`SortedSet.symmetric_difference`.

.. image:: _static/SortedSet_runtime-symmetric_difference_small.png

symmetric_difference_tiny
.........................

Set symmetric-difference using :func:`SortedSet.symmetric_difference`.

.. image:: _static/SortedSet_runtime-symmetric_difference_tiny.png

symm_diff_update_large
......................

Set symmetric-difference using :func:`SortedSet.symmetric_difference_update`.

.. image:: _static/SortedSet_runtime-symmetric_difference_update_large.png

symm_diff_update_medium
.......................

Set symmetric-difference using :func:`SortedSet.symmetric_difference_update`.

.. image:: _static/SortedSet_runtime-symmetric_difference_update_medium.png

symm_diff_update_small
......................

Set symmetric-difference using :func:`SortedSet.symmetric_difference_update`.

.. image:: _static/SortedSet_runtime-symmetric_difference_update_small.png

symm_diff_update_tiny
.....................

Set symmetric-difference using :func:`SortedSet.symmetric_difference_update`.

.. image:: _static/SortedSet_runtime-symmetric_difference_update_tiny.png
