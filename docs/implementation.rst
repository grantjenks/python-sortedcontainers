Implementation Details
======================

The :doc:`Sorted Containers<index>` internal implementation is based on a
couple observations. The first is that Python's `list` is fast, *really
fast*. Lists have great characteristics for memory management and random
access. The second is that `bisect.insort` is fast. This is somewhat
counter-intuitive since it involves shifting a series of items in a list. But
modern processors do this really well. A lot of time has been spent optimizing
mem-copy/mem-move-like operations both in hardware and software.

But using only one list and `bisect.insort` would produce sluggish behavior for
lengths exceeding ten thousand. So the implementation of :doc:`sortedlist` uses
a list of lists to store elements. In this way, inserting or deleting is most
often performed on a short list. Only rarely does a new list need to be added
or deleted.

:doc:`sortedlist` maintains three internal variables: `_lists`, `_maxes`, and
`_index`. The first is simply the list of lists, each member is a sorted
sublist of elements. The second contains the maximum element in each of the
sublists. This is used for fast binary-search. The last maintains a tree of
pair-wise sums of the lengths of the lists.

Lists are kept balanced using the load factor. If a sublist's length exceeds
double the load then it is split in two. Likewise at half the load it is
combined with its neighbor. By default this factor is 1,000 which seems to work
well for lengths up to ten million. Lengths above that are recommended a load
factor that is the square root to cube root of the average length.  (Although
you will probably exhaust the memory of your machine before that point.)
Experimentation is also recommended. A :doc:`load factor performance
comparison<performance-load>` is also provided. For more in-depth analysis,
read :doc:`performance-scale` which benchmarks :doc:`Sorted Containers<index>`
with ten billion elements.

Finding an element is a two step process. First the `_maxes` list, also known
as the "maxes" index, is bisected which yields the position of a sorted
sublist. Then that sublist is bisected for the location of the element.

Compared to tree-based implementations, using lists of lists has a few
advantages based on memory usage.

1. Most insertion/deletion doesn't require allocating or freeing memory. This
   can be a big win as it takes a lot of strain off the garbage collector and
   memory system.
2. Pointers to elements are packed densely. A traditional tree-based
   implementation would require two pointers (left/right) to child nodes. Lists
   have no such overhead. This benefits the hardware's memory architecture and
   more efficiently utilizies caches.
3. The memory overhead per item is effectively a pointer to the item. Binary
   tree implementations must add at least two more pointers per item.
4. Iteration is extremely fast as sequentially indexing lists is a strength of
   modern processors.

Traditional tree-based designs have better big-O notation but that ignores the
realities of today's software and hardware. For a more in-depth analysis, read
:doc:`Performance at Scale<performance-scale>`.

Indexing uses the `_index` list which operates as a tree of pair-wise sums of
the lengths of the lists. The tree is maintained as a dense binary tree. It's
easiest to explain with an example. Suppose `_lists` contains sublists with
these lengths (in this example, we assume the load factor is 4)::

    list(map(len, _lists)) -> [3, 5, 4, 5, 6]

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
so are contained in the docstring for `SortedList._loc` and `SortedList._pos`.

For example, indexing requires traversing the tree to a leaf node. Each node
has two children which are easily computable. Given an index, `pos`, the
left-child is at ``pos * 2 + 1`` and the right-child is at ``pos * 2 + 2``.

When the index is less than the left-child, traversal moves to the left
sub-tree. Otherwise, the index is decremented by the left-child and traversal
moves to the right sub-tree.

At a leaf node, the indexing pair is computed from the relative position of the
node as compared with the offset and the remaining index.

For example, given the following index::

    _index = 14 5 9 3 2 4 5
    _offset = 3

    Tree:

             14
          5      9
        3   2  4   5

Indexing position 8 involves iterating like so:

1. Starting at the root, position 0, 8 is compared with the left-child node (5)
   which it is greater than. When greater, the index is decremented and the
   position is updated to the right child node.
2. At node 9 with index 3, we again compare the index to the left-child node
   with value 4. Because the index is the less than the left-child node, we
   simply traverse to the left.
3. At node 4 with index 3, we recognize that we are at a leaf node and stop
   iterating.
4. To compute the sublist index, we subtract the offset from the index of the
   leaf node: ``5 - 3 = 2``. To compute the index in the sublist, we simply use
   the index remaining from iteration. In this case, 3.

The final index pair from our example is (2, 3) which corresponds to index 8 in
the sorted list.

Maintaining the position index in this way has several advantages:

* It's easy to traverse to children/parent. The children of a position in the
  `_index` are at ``(pos * 2) + 1`` and ``(pos * 2) + 2``. The parent is at
  ``(pos - 1) // 2``. We can even identify left/right-children easily. Each
  left-child is at an odd index and each right-child is at an even index.

* It's not built unless needed. If no indexing occurs, the memory and time
  accounting for position is skipped.

* It's fast to build. Calculating sums pair-wise and concatenating lists can
  all be done within C-routines in the Python interpreter.

* It's space efficient. The whole index is no more than twice the size of the
  length of the `_lists` and contains only integers.

* It's easy to update. Adding or removing an item involves incrementing or
  decrementing only ``log2(len(_index))`` items in the index. The only caveat
  to this is when a new sublist is created/deleted. In those scenarios the
  entire index is deleted and not rebuilt until needed.

The construction and maintenance of the positional index is unusual compared
to other traditional designs. Whether the design is novel, I (Grant Jenks) do
not know. Until shown otherwise, I would like to refer to it as the "Jenks"
index.

Each sorted container has a function named `_check` for verifying
consistency. This function details the data-type invariants.
