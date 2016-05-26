Implementation Details
======================

The sorted container types are implemented based on a couple observations. The
first is that Python lists are fast, really fast. They have great
characteristics for memory management and random access. The second is that
bisect.insort is fast. This is somewhat counter-intuitive since it ultimately
involves shifting a series of items in a list. But modern processors do this
really well. A lot of time has been spent optimizing memcopy/memmove-like
operations both in hardware and software.

But using only one list and bisect.insort would produce sluggish behavior for
lengths exceeding ten thousand. So the implementation of SortedList uses a list
of lists to store values. In this way, inserting or deleting is most often
performed on a short list. Only rarely does a new list need to be added or
deleted.

SortedList maintains three internal variables: _lists, _maxes, and _index. The
first is simply the list of lists. Each element is a list containing items. The
second contains the maximum value in each of the lists. This is used for fast
binary-search. The last maintains a tree of pair-wise sums of the lengths of
the lists.

Lists are kept balanced using the _load factor. If an internal list's length
exceeds double the load then it is split in two. Likewise at half the load it
is combined with its neighbor. By default this factor is 1000 which seems to
work well for lengths up to ten million. Lengths above that are recommended a
load factor that is the square root of the average length (although you will
probably exhaust the memory of your machine before that point). Experimentation
is also recommended. A :doc:`load factor performance
comparison<performance-load>` is also provided.

Finding an element is a two step process. First the _maxes list is bisected
which yields the index of a short sorted list. Then that list is bisected for
the index of the element.

Compared to tree-based implementations, using lists of lists has a few
advantages based on memory usage.

1. Most insertion/deletion doesn't require allocating or freeing memory. This
can be a big win as it takes a lot of strain off the garbage collector and
memory system.

2. Pointers to elements are packed densely. A traditional tree-based
implementation would require two pointers (left/right) to child nodes. Arrays
have no such overhead. This benefits the hardware's memory architecture and
better leverages caching.

3. The memory overhead per item is effectively a pointer to the item. Binary
tree implementations must add at least two more pointers per item.

4. Iteration is extremely fast as indexing sequential elements is a strength of
modern processors.

Traditional tree-based designs have better big-O notation but that ignores the
realities of today's software and hardware.

Indexing uses the _index list which operates as a tree of pair-wise sums of the
lengths of the lists. The tree is maintained as a dense binary tree. It's
easiest to explain with an example. Suppose _lists contains sublists with these
lengths (in this example, we assume the _load parameter is 4)::

    map(len, _lists) -> [3, 5, 4, 5, 6]

Given these lengths, the first row in the index is the pair-wise sums::

    [8, 9, 6, 0]

We pad the first row with zeros to make its length a power of 2. The next rows
of sums work similarly::

    [17, 6]
    [23]

Then all the rows are concatenated in reverse order so that the index is
finally::

    [23, 17, 6, 8, 9, 6, 0, 3, 5, 4, 5, 6]

With this list, we can efficiently compute the index of an item in a sublist
and, vice-versa, find an item given an index. Details of the algorithms to do
so are contained in the docstring for SortedList._loc and
SortedList._pos. Maintaining the position index in this way has several
advantages:

* It's easy to traverse to children/parent. The children of a position in the
  _index are at (pos * 2) + 1 and (pos * 2) + 2. The parent is at (pos - 1)
  // 2. We can even identify left/right-children easily. Each left-child is at
  an odd index and each right-child is at an even index.

* It's not built unless needed. If no indexing occurs, the memory and time
  accounting for position is skipped.

* It's fast to build. Calculating sums pair-wise and concatenating lists can
  all be done within C-routines in the Python interpreter.

* It's space efficient. The whole index is no more than twice the size of the
  length of the _lists and contains only integers.

* It's easy to update. Adding or removing an item involves incrementing or
  decrementing only log(len(_index)) items in the index. The only caveat to
  this is when a new sublist is created/deleted. In those scenarios the entire
  index is deleted and not rebuilt until needed.

The construction and maintainence of the index is unusual compared to other
designs described in research. Whether the design is novel, I (Grant Jenks) do
not know. I based the dense-tree structure on the efficiency of the heapq
module in Python.

Each sorted container has a function named _check for verifying
consistency. This function details the data-type invariants.
