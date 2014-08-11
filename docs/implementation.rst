Implementation Details
======================

The sorted container types are implemented based on a single observation:
bisect.insort is fast, really fast. This is somewhat counter-intuitive since
most schools teach that shifting elements in an array is slow. But modern
processors do this really well. A lot of time has been spent optimizing
memcopy/memmove-like operations both in hardware and software.

But using only one list and bisect.insort would produce sluggish behavior for
lengths exceeding one thousand. So the implementation of SortedList uses a list
of lists to store values. In this way, inserting or deleting is most often
performed on a short list. Only rarely does a new list need to be added or
deleted.

SortedList maintains three internal variables: _lists, _maxes, and _index. The
first is simply the list of lists. Each element is a list containing items. The
second contains the maximum value in each of the lists. This is used for fast
binary-search. The last contains a cumulative sum of the lengths of the
lists. With that we can index efficiently.

Lists are kept balanced using the _load factor. If an internal list's length
exceeds double the load then it is split in two. Likewise at half the load it is
combined with its neighbor. By default this factor is 1000 which seems to work
well for lengths up to about ten million. Lengths above that are recommended a
load factor that is the square or cube root of the average length. So for a list
of a billion elements, a load factor of one thousand should be
efficient. Experimentation is also recommended. A :doc:`load factor performance
comparison<performance-load>` is also provided.

Finding an element is a two step process. First the _maxes list is bisected
which yields the index of a short sorted list. Then that list is bisected for
the index of the element.

Indexing uses the _index list which operates as a cache of the cumulative sum of
the lengths of the lists. Indexing requires bisecting the _index list and then
indexing the appropriate sub-list. Adding or removing elements invalidates the
cache so efficient maintenance is required.

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

Tree-based designs have better big-O notation but that ignores the realities of
today's software and hardware.

Each sorted container has a function named _check for verifying consistency.
