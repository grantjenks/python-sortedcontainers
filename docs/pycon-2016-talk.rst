Python Sorted Collections - PyCon 2016 Talk
===========================================

* `Python Sorted Collections Video Recording on Youtube`_
* `Python Sorted Collections Slides`_

Hello, I’m here today to talk about `Python sorted collections`_. I’m excited
and a bit nervous to be up here in front of all you smart people. But I’m a
pretty smart guy myself and I really admire Python so let’s get started.

Every time I talk about `sorted collections`_, my wife hear’s sordid. We’ll see
today how many times I can confuse the on-site captioners. You’re probably more
familiar with sorted collections than you realize.

In the standard library we have `heapq`_, `bisect`_ and `queue.PriorityQueue`_
but they don't quite fill the gap. Behind the scenes, priority queue uses a
heap implementation. Another common mistake is to think that
`collections.OrderedDict`_ is a dictionary that maintains sort order but that’s
not the case.

I don't always import sorted types. But when I do, I expect them in the
standard library.

And here’s why. `Java`_, `C++`_ and `.NET`_ have them. `Python`_ has broken
into the top five of the TIOBE index but feels a bit more like `PHP`_ or
`Javascript`_ in this regard.

We also depend on external solutions: `Sqlite in-memory indexes`_,
`pandas.DataFrame indexes`_, and `Redis sorted sets`_. If you’ve ever issued a
“zadd” command to Redis then you used a sorted collection.

So what should be the API of sorted collection types in Python?

Well, a sorted list should be a `MutableSequence`_. Pretty close to the “list”
API. But there’s a sort order constraint that must be satisfied by “setitem”
and “insert” methods. Also should support a “key” argument like the “sorted”
builtin function. Given sorted order, “bisect_right” and “bisect_left” methods
make sense. You could also imagine an “add” method and “discard” method for
elements. Kind of like a multi-set in other languages. I’d also expect
“getitem”, “contains”, “count”, etc. to be faster than linear time.

A sorted dictionary should be a `MutableMapping`_. Pretty close to the
dictionary API. But iteration yields items in sorted order. Also should support
efficient positional indexing, something like a SequenceView.

Sorted set should be a `MutableSet`_. Pretty close to the “set” API. Sorted set
should also be a Sequence like the “tuple” API to support efficient positional
indexing.

The chorus and the refrain from core developers is: "Look to the `PyPI`_."
Which is good advice.

So let’s talk about your options with a bit of software archaeology.

`Blist`_ is the genesis of our story but it wasn’t really designed for sorted
collections. It’s written in C and the innovation here is the “blist” data
type. That’s a B-tree based replacement for CPython’s built-in list. Sorted
list, sorted dictionary, and sorted set were built on top of this “blist” data
type and it became the incumbent to beat. Also noteworthy is that the API was
rather well thought out.

There were some quirks; for example: the “pop” method returns the first element
rather than the last element in the sorted list.

`SortedCollection`_ is not a package. You can’t install this with “pip”. It’s
simply a Python recipe that Raymond Hettinger linked from the Python
docs. Couple innovations here though: it’s simple, it’s written in pure-Python,
and maintains a parallel list of keys. So we have efficient support for that
key-function parameter.

This is `bintrees`_. Still alive and kicking today. A few innovations here:
it’s written with Cython support to improve performance and has a few different
tree “backends.” You can create a red-black or AVL-tree depending on your
needs. There’s also some notion of accessing the nodes themselves and
customizing the tree traversal to slice by value rather than by index.

`Banyan`_ had a very short life but adds another couple innovations: it’s
incredibly fast and achieves that through C++ template meta-programming. It
also has a feature called tree-augmentation that will let you store metadata at
tree nodes. You can use this for interval trees if you need those.

Finally there’s `skiplistcollections`_. Couple significant things here: it’s
pure-Python but fast, even for large collections, and it uses a skip-list data
type rather than a binary tree.

Altogether, you go on PyPI and try to figure this out and it’s kind of like
this. It’s a mess. PyPI has really got to work better than using `Google`_ with
the site operator.

Couple others worth calling out: `rbtree`_ is another fast C-based
implementation. And there’s a few like treap, splay and scapegoat that are
contributions and experiments by `Dan Stromberg`_. He’s also done some
interesting benchmarking of the various tree types. There’s no silver bullet
when it comes to trees.

I love Python because there's one right way to do things. If I just want sorted
types, what’s the right answer?

I couldn’t find the right answer so I built it. The missing battery: `Sorted
Containers`_.

Here it is. This is the project home page. `Sorted Containers`_ is a `Python
sorted collections`_ library with `sorted list`_, `sorted dictionary`_, and
`sorted set`_ implementations. It’s pure-Python but it’s as fast as
C-extensions. It’s Python 2 and Python 3 compatible. It’s fully-featured. And
it’s extensively tested with 100% coverage and hours of stress.

`Performance`_ is a feature. That means graphs. Lot’s of them. There are 189
performance graphs in total. Let’s look at a few of them together.

Here’s the performance of adding a random value to a sorted list. I’m comparing
`Sorted Containers`_ with other competing implementations.

Notice the axes are log-log. So if performance differs by major tick marks then
one is actually ten times faster than the other.

We see here that `Sorted Containers`_ is in fact about ten times faster than
blist when it comes to adding random values to a sorted list. Notice also
Raymond’s recipe is just a list and that displays order n-squared runtime
complexity. That’s why it curves upwards.

Of all the sorted collections libraries, `Sorted Containers`_ is also fastest
at initialization. We’ll look at why soon.

`Sorted Containers`_ is not always fastest. But notice here the performance
improves with scale. You can see it there in blue. It starts in the middle of
the pack and has a lesser slope than competitors.

In short, `Sorted Containers`_ is kind of like a `B-tree`_ implementation. That
means you can configure the the fan-out of nodes in the tree. We call that the
load parameter and there are extensive performance graphs of three different
`load parameters`_.

Here we see that a load factor of ten thousand is fastest for indexing a sorted
list.

Notice the axes now go up to ten million elements. I’ve actually scaled
`SortedList`_ all the way to ten billion elements. It was a really incredible
experiment. I had to rent the largest high-memory instance available from
Google Compute Engine. That benchmark required about 128 gigabytes of memory
and cost me about thirty dollars.

This is the performance of deleting a key from a sorted dictionary. Now the
smaller load-factor is fastest. The default load-factor is 1,000 and works well
for most scenarios. It’s a very sane default.

In addition to comparisons and load-factors, I also `benchmark
runtimes`_. Here’s CPython 2.7, CPython 3.5 and `PyPy`_ version 5. You can see
where the the just-in-time compiler, the jit-compiler, kicks in. That’ll make
`Sorted Containers`_ another ten times faster.

Finally, I made a survey in 2015 on `Github`_ as to how people were using
sorted collections. I noticed patterns like priority queues, mutli-sets,
nearest-neighbor algorithms, etc.

This is the priority queue workload which spends 40% of its time adding
elements, 40% popping elements, 10% discarding elements, and has a couple other
methods.

`Sorted Containers`_ is two to ten times faster in all of these scenarios.

We also have a lot of features. The API is nearly a drop-in replacement for the
“blist” and “rbtree” modules. But the quirks have been fixed so the “pop”
method returns the last element rather than the first.

Sorted lists are sorted so you can bisect them. Looking up the index of an
element is also very fast.

Bintrees introduced methods for tree traversal. And I’ve boiled those down to a
couple API methods. On line 3, we see “irange”. Irange iterates all keys from
bob to eve in sorted order.

Sorted dictionaries also have a sequence-like view called iloc. If you’re
coming from Pandas that should look familiar. Line 4 creates a list of the five
largest keys in the dictionary.

Similar to “irange” there is an “islice” method. Islice does positional index
slicing. In line 5 we create an iterator over the indexes 10 through 49
inclusive.

One of the benefits of being pure-Python: it’s easy to hack on. Over the years,
a few patterns have emerged and become recipes. All of these are available from
PyPI with pip install `sortedcollections`_.

If all that didn’t convince you that `Sorted Containers`_ is great then listen
to what `other smart people say`_ about it:

Alex Martelli says: Good stuff! ... I like the simple, effective implementation
idea of splitting the sorted containers into smaller “fragments” to avoid the
O(N) insertion costs.

Jeff Knupp writes: That last part, “fast as C-extensions,” was difficult to
believe. I would need some sort of performance comparison to be convinced this
is true. The author includes this in the docs. It is.

Kevin Samuel says: I’m quite amazed, not just by the code quality (it’s
incredibly readable and has more comment than code, wow), but the actual amount
of work you put at stuff that is not code: documentation, benchmarking,
implementation explanations. Even the git log is clean and the unit tests run
out of the box on Python 2 and 3.

If you’re new to sorted collections, I hope I’ve piqued your interest. Think
about the achievement here. `Sorted Containers`_ is pure-Python but as fast as
C-implementations. Let’s look under the hood of `Sorted Containers`_ at what
makes it so fast.

It really comes down to bisect for the heavy lifting. Bisect is a module in the
standard library that implements binary search on lists. There’s also a handy
method called insort that does a binary search and insertion for us in one
call. There’s no magic here, it’s just implemented in C and part of the
standard library.

Here’s the basic structure. It’s just a list of sublists. So there’s a member
variable called “lists” that points to sublists. Each of those is maintained in
sorted order. You’ll sometimes hear me refer to these as the top-level list and
its sublists.

There’s no need to wrap sublists in their own objects. They are just
lists. Simple is fast and efficient.

In addition to the list of sublists. There’s an index called the maxes
index. That simply stores the maximum value in each sublist. Now lists in
CPython are simply arrays of pointers so we’re not adding much overhead with
this index.

Let’s walk through testing membership with contains. Let’s look for element 14.

Let’s also walk through adding an element. Let’s add 5 to the sorted list.

Now numeric indexing is a little more complex. Numeric indexing uses a tree
packed densely into another list. I haven’t seen this structure described in
textbooks or research so I’d like to call it a “Jenks” index. But I’ll also
refer to it as the positional index.

Let’s build the positional index together.

Remember the positional index is a tree stored in a list, kind of like a heap.

Let’s use this to lookup index 8. Starting at the root, 18, compare index to
the left-child node. 8 is greater than 7 so we subtract 7 from 8 and move to
the right-child node. Again, now at node 11, compare index again to the
left-child node. 1 is less than 6, so we simply move to the left-child node. We
terminate at 6 because it’s a leaf node. Our final index is 1 and our final
position is 5. We calculate the top-level list index as the position minus the
offset. So our final coordinates are index 2 in the top-level list and index 1
in the sublist.

That’s it. Three lists maintain the elements, the maxes index, and the
positional index. We’ve used simple built-in types to construct complex
behavior.

Altogether that gets us to our first performance lesson.

Builtin types are fast. Like really fast. Builtin types are as fast as C and
benefit from years of optimizations.

Ok, let’s look at the contains method for a sorted list. This is the majority
of the code. We bisect the maxes index for the sublist index. Then we bisect
the sublist for the element index.

How many lines of Python code execute? 4.

How many instructions execute? Hundreds of lines of C-code.

Rather than programming in Python, I programmed against my interpreter. That’s
our next lesson.

Program your interpreter. The operations provided by the interpreter and
standard library are fast. They’re implemented in C. When you program your
interpreter, you write C code but in Python.

Now let’s talk about memory. This is very simplified. My apologies to those who
feel this is grossly simplified. Notice the limited sizes: a dozen registers,
kilobytes of L1 cache, megabytes of L3 cache. Some machines don’t even have an
L3 cache.

So keep overhead low. Keep related data packed together. Our sublists add
roughly one pointer per element. That’s all. It’s 66% less memory than binary
tree implementations.

Also, each memory tier has different performance. Memory slows down by a factor
of a thousand from registers to main memory. And the advertised price of memory
lookups is often the average random lookup time. But that’s only one common
pattern.

Sequential memory access patterns are so fast you almost don’t pay for them at
all. The processor predicts the memory you’ll need next and queues it for you.

Then there’s also data-dependent memory accesses which happen when you follow
pointers. So the next memory location is dependent on the current one. This is
typical in binary trees and it’s really slow. It’s as much as ten times slower
than random memory access.

Let’s think about adding elements again. Add calls bisect.insort which does a
binary search and then insert on the list.

Here is the code for insert in CPython. It is entirely sequential memory
accesses. Also the binary search process starts random but narrows the search
range and so improves locality of memory accesses.

By comparison, traditional binary trees use data-dependent memory access as
they repeatedly dereference pointers. We can sequentially shift a thousand
elements in memory in the time it takes to access a couple of binary nodes from
DRAM.

So memory is tiered. And caches are limited in size.

This is also why the slope of the performance curve for sorted list was less
than that for binary tree implementations. At scale, binary trees do more
data-dependent DRAM lookups than `Sorted Containers`_.

I said that initializing a sorted container is fast. Let’s look at why. Here’s
the initializer for a `SortedList`_. Notice it simply calls the sorted builtin
and then chops up the result into sublists and then initializes the maxes
index.

I think of this as a cheat. I’m using the power of `Timsort`_ to initialize the
container. And it turns out initialization is really common. The result is fast
and readable.

Also, how long does it take to initialize already sorted data? Linear
time. It’s just a couple mem-copy like operations.

Here’s another cheat. When we add an element to a sorted set, we add it to both
a set object and sorted list. This preserves the fast set membership tests.

Some purists will argue that `hashing`_ should not be necessary. They are
correct, but, if you can define comparisons, then you can probably define
hash. Remember that we’re solving real problems, not theoretical ones. If you
can reuse the builtin types, then cheat and do it.

So, if you can, cheat. The way to make things faster is to do less
work. There’s no way around that.

Another cheat I’ve mentioned regards the positional index. If you don’t need
numerical lookups, then don’t build the index. That’s a common scenario with
sorted dictionaries. We use less memory and run faster.

When it comes to runtime complexity, here’s the punchline: adding random
elements has an amortized cost proportional to the cube root of the container
size. That’s an unusual runtime complexity but it works quite well.

The surprising thing is that “n” stays relatively small in practice. For
example, creating a billion integers in CPython will take more than 30
gigabytes of memory which is already exceeding the limits of most machines.

We’ve also seen that memory is expensive. Allocations are costly. In the common
case, `Sorted Containers`_ allocates no more memory when adding elements.

If you’re doubtful about performance at scale, then I encourage you to read the
project docs. There’s a page called `Performance at Scale`_ and it talks
extensively about theory with benchmarks up to ten billion elements.

A little PSA before I continue: If you claim to be fast, you’ve got to have
measurements. Measure. Measure. Measure. `Big-O notation`_ is not a substitute
for benchmarks. Quite often, constants and coefficients that are ignored in
theory matter quite a lot in practice.

So: Measure. Measure. Measure.

This whole project in fact started with a measurement. I was timing how long it
took to add an element to a “blist” when I noticed that “bisect.insort” was
actually faster for a list with one thousand elements. It was so much faster in
fact, I thought “wow, I could do two inserts in a thousand-element list and
still be faster than “blist.” That thought eventually became the list of
sublists implementation that we have today.

So here’s the performance lessons: builtin types are fast; program your
interpreter; memory is tiered; cheat, if you can; and measure, measure,
measure.

A couple closing thoughts. Everything related to `Sorted Containers`_ is under
an open-source `Apache2 license`_. Contributors are very welcome. We’ve started
to create a little community around sorted collections.

I think it’s interesting to ask: is this worth a PEP? I’m personally on the
fence. I think sorted collections would contribute to Python’s maturity. But I
don’t know if any proposal could survive the inevitable bike-shedding. My
contribution is a pure-Python implementation that’s fast-enough for most
scenarios.

I’ll end with a quote from `Mark Summerfield`_. Mark and a couple other authors
have actually deprecated their modules in favor of `Sorted Containers`_. Mark
says: “Python’s ‘batteries included’ standard library seems to have a battery
missing. And the argument that ‘we never had it before’ has worn thin. It is
time that Python offered a full range of collection classes out of the box,
including sorted ones.”

Thanks for letting me share.

.. _`Python Sorted Collections Video Recording on Youtube`: https://www.youtube.com/watch?v=7z2Ki44Vs4E
.. _`Python Sorted Collections Slides`: http://bit.ly/soco-pycon
.. _`Python sorted collections`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`heapq`: https://docs.python.org/3/library/heapq.html
.. _`bisect`: https://docs.python.org/3/library/bisect.html
.. _`queue.PriorityQueue`: https://docs.python.org/3/library/queue.html#queue.PriorityQueue
.. _`collections.OrderedDict`: https://docs.python.org/3/library/collections.html#collections.OrderedDict
.. _`Sqlite in-memory indexes`: https://www.sqlite.org/lang_createindex.html
.. _`pandas.DataFrame indexes`: http://pandas.pydata.org/pandas-docs/stable/indexing.html
.. _`Redis sorted sets`: https://redis.io/topics/data-types
.. _`MutableSequence`: https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
.. _`PyPI`: https://pypi.org/
.. _`Dan Stromberg`: http://stromberg.dnsalias.org/~dstromberg/datastructures/
.. _`B-tree`: https://en.wikipedia.org/wiki/B-tree
.. _`PyPy`: http://pypy.org/
.. _`Github`: https://github.com/
.. _`Blist`: http://stutzbachenterprises.com/blist/
.. _`SortedCollection`: http://code.activestate.com/recipes/577197-sortedcollection/
.. _`bintrees`: https://pypi.org/project/bintrees/
.. _`Sorted Containers`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`Banyan`: https://pythonhosted.org/Banyan/
.. _`skiplistcollections`: https://pypi.org/project/skiplistcollections/
.. _`Google`: https://www.google.com/
.. _`rbtree`: https://pypi.org/project/rbtree/
.. _`Sorted Containers`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`sorted list`: http://www.grantjenks.com/docs/sortedcontainers/sortedlist.html
.. _`sorted dictionary`: http://www.grantjenks.com/docs/sortedcontainers/sorteddict.html
.. _`sorted set`: http://www.grantjenks.com/docs/sortedcontainers/sortedset.html
.. _`SortedList`: http://www.grantjenks.com/docs/sortedcontainers/sortedlist.html
.. _`Performance`: http://www.grantjenks.com/docs/sortedcontainers/performance.html
.. _`Timsort`: https://en.wikipedia.org/wiki/Timsort
.. _`hashing`: https://en.wikipedia.org/wiki/Hash_function
.. _`Big-O notation`: https://en.wikipedia.org/wiki/Big_O_notation
.. _`Apache2 license`: http://www.apache.org/licenses/LICENSE-2.0
.. _`Mark Summerfield`: http://www.qtrac.eu/pysorted.html
.. _`benchmark runtimes`: http://www.grantjenks.com/docs/sortedcontainers/performance-runtime.html
.. _`sortedcollections`: http://www.grantjenks.com/docs/sortedcollections/
.. _`other smart people say`: http://www.grantjenks.com/docs/sortedcontainers/#testimonials
.. _`Performance at Scale`: http://www.grantjenks.com/docs/sortedcontainers/performance-scale.html
.. _`sorted collections`: http://www.grantjenks.com/docs/sortedcontainers/
.. _`Java`: https://www.java.com/
.. _`C++`: https://isocpp.org/
.. _`.NET`: https://www.microsoft.com/net
.. _`Python`: https://www.python.org/
.. _`PHP`: http://php.net/
.. _`Javascript`: https://en.wikipedia.org/wiki/ECMAScript
.. _`MutableMapping`: https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
.. _`MutableSet`: https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
.. _`load parameters`: http://www.grantjenks.com/docs/sortedcontainers/performance-load.html
