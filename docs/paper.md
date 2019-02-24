---
title: 'Python Sorted Containers'
tags:
  - Python
  - sorted
  - list
  - dictionary
  - set
authors:
  - name: Grant Jenks
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
 - name: Lyman Spitzer, Jr. Fellow, Princeton University
   index: 1
date: 23 February 2019
bibliography: paper.bib
---

# Summary

You’re probably more familiar with sorted collections than you realize.

In the standard library we have heapq, bisect and queue.PriorityQueue but they
don’t quite fill the gap. Behind the scenes, priority queue uses a heap
implementation. Another common mistake is to think that collections.OrderedDict
is a dictionary that maintains sort order but that’s not the case.

I don’t always import sorted types. But when I do, I expect them in the
standard library.

And here’s why. Java, C++ and .NET have them. Python has broken into the top
five of the TIOBE index but feels a bit more like PHP or Javascript in this
regard.

We also depend on external solutions: Sqlite in-memory indexes,
pandas.DataFrame indexes, and Redis sorted sets. If you’ve ever issued a “zadd”
command to Redis then you used a sorted collection.

So what should be the API of sorted collection types in Python?

Well, a sorted list should be a MutableSequence. Pretty close to the “list”
API. But there’s a sort order constraint that must be satisfied by “setitem”
and “insert” methods. Also should support a “key” argument like the “sorted”
builtin function. Given sorted order, “bisect_right” and “bisect_left” methods
make sense. You could also imagine an “add” method and “discard” method for
elements. Kind of like a multi-set in other languages. I’d also expect
“getitem”, “contains”, “count”, etc. to be faster than linear time.

A sorted dictionary should be a MutableMapping. Pretty close to the dictionary
API. But iteration yields items in sorted order. Also should support efficient
positional indexing, something like a SequenceView.

Sorted set should be a MutableSet. Pretty close to the “set” API. Sorted set
should also be a Sequence like the “tuple” API to support efficient positional
indexing.

The chorus and the refrain from core developers is: “Look to the PyPI.” Which
is good advice.

So let’s talk about your options with a bit of software archaeology.

Blist is the genesis of our story but it wasn’t really designed for sorted
collections. It’s written in C and the innovation here is the “blist” data
type. That’s a B-tree based replacement for CPython’s built-in list. Sorted
list, sorted dictionary, and sorted set were built on top of this “blist” data
type and it became the incumbent to beat. Also noteworthy is that the API was
rather well thought out.

There were some quirks; for example: the “pop” method returns the first element
rather than the last element in the sorted list.

SortedCollection is not a package. You can’t install this with “pip”. It’s
simply a Python recipe that Raymond Hettinger linked from the Python
docs. Couple innovations here though: it’s simple, it’s written in pure-Python,
and maintains a parallel list of keys. So we have efficient support for that
key-function parameter.

This is bintrees. Still alive and kicking today. A few innovations here: it’s
written with Cython support to improve performance and has a few different tree
“backends.” You can create a red-black or AVL-tree depending on your
needs. There’s also some notion of accessing the nodes themselves and
customizing the tree traversal to slice by value rather than by index.

Banyan had a very short life but adds another couple innovations: it’s
incredibly fast and achieves that through C++ template meta-programming. It
also has a feature called tree-augmentation that will let you store metadata at
tree nodes. You can use this for interval trees if you need those.

Finally there’s skiplistcollections. Couple significant things here: it’s
pure-Python but fast, even for large collections, and it uses a skip-list data
type rather than a binary tree.

Altogether, you go on PyPI and try to figure this out and it’s kind of like
this. It’s a mess. PyPI has really got to work better than using Google with
the site operator.

Couple others worth calling out: rbtree is another fast C-based
implementation. And there’s a few like treap, splay and scapegoat that are
contributions and experiments by Dan Stromberg. He’s also done some interesting
benchmarking of the various tree types. There’s no silver bullet when it comes
to trees.

I love Python because there’s one right way to do things. If I just want sorted
types, what’s the right answer?

I couldn’t find the right answer so I built it. The missing battery: Sorted
Containers.

Here it is. This is the project home page. Sorted Containers is a Python sorted
collections library with sorted list, sorted dictionary, and sorted set
implementations. It’s pure-Python but it’s as fast as C-extensions. It’s Python
2 and Python 3 compatible. It’s fully-featured. And it’s extensively tested
with 100% coverage and hours of stress.

Performance is a feature. That means graphs. Lot’s of them. There are 189
performance graphs in total. Let’s look at a few of them together.

Here’s the performance of adding a random value to a sorted list. I’m comparing
Sorted Containers with other competing implementations.

Notice the axes are log-log. So if performance differs by major tick marks then
one is actually ten times faster than the other.

We see here that Sorted Containers is in fact about ten times faster than blist
when it comes to adding random values to a sorted list. Notice also Raymond’s
recipe is just a list and that displays order n-squared runtime
complexity. That’s why it curves upwards.

Of all the sorted collections libraries, Sorted Containers is also fastest at
initialization. We’ll look at why soon.

Sorted Containers is not always fastest. But notice here the performance
improves with scale. You can see it there in blue. It starts in the middle of
the pack and has a lesser slope than competitors.

In short, Sorted Containers is kind of like a B-tree implementation. That means
you can configure the the fan-out of nodes in the tree. We call that the load
parameter and there are extensive performance graphs of three different load
parameters.

Here we see that a load factor of ten thousand is fastest for indexing a sorted
list.

Notice the axes now go up to ten million elements. I’ve actually scaled
SortedList all the way to ten billion elements. It was a really incredible
experiment. I had to rent the largest high-memory instance available from
Google Compute Engine. That benchmark required about 128 gigabytes of memory
and cost me about thirty dollars.

This is the performance of deleting a key from a sorted dictionary. Now the
smaller load-factor is fastest. The default load-factor is 1,000 and works well
for most scenarios. It’s a very sane default.

In addition to comparisons and load-factors, I also benchmark runtimes. Here’s
CPython 2.7, CPython 3.5 and PyPy version 5. You can see where the the
just-in-time compiler, the jit-compiler, kicks in. That’ll make Sorted
Containers another ten times faster.

Finally, I made a survey in 2015 on Github as to how people were using sorted
collections. I noticed patterns like priority queues, mutli-sets,
nearest-neighbor algorithms, etc.

This is the priority queue workload which spends 40% of its time adding
elements, 40% popping elements, 10% discarding elements, and has a couple other
methods.

Sorted Containers is two to ten times faster in all of these scenarios.

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
PyPI with pip install sortedcollections.

If all that didn’t convince you that Sorted Containers is great then listen to
what other smart people say about it:

Alex Martelli says: Good stuff! … I like the simple, effective implementation
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
about the achievement here. Sorted Containers is pure-Python but as fast as
C-implementations. Let’s look under the hood of Sorted Containers at what makes
it so fast.

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

# Acknowledgements

Thank you to the open source community that has contributed bug reports,
documentation improvements, and feature guidance in development of the project.

Significant interface design credit is due to Daniel Stutzbach and the "blist"
software project which this project originally copied.

# References
