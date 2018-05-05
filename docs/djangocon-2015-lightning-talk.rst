DjangoCon 2015 Lightning Talk
=============================

* `Accompanying Slides`_

Welcome. I'm excited to be here today. My name is Grant Jenks and I've been
working with Python since about 2011. Like many of you, I was pleasantly
surprised and impressed by Python's "batteries included" slogan.

Not long into Python development, I started asking questions like these:
* "How do you sort a Python dictionary by value?"
* "How do I get the maximum value in a dictionary?"
* "Can I somehow search a dictionary's keys?"
These questions get viewed millions of times for every priority queue, or
cache, or in-memory index, or even indexable set that somebody needs.

In response, I got some great answers. The first was OrderedDict. But you
quickly learn that ordered isn't the same as sorted.

And then there was Counter. It gets combined with another module, heapq, which
can maintain a binary heap.

All of these were wonderfully fast except when they weren't. They all kind
of assume that updates can be batched and sorted methods can work lazily.
And that gets us really far. Really far. But sometimes you want more.

So if C++ and Java and .NET all have sorted map-like data types, why doesn't
Python? I found the answer from Nick Coghlan paraphrasing Guido: “if a user is
sophisticated enough to realise that the builtin types aren't the right
solution for their problem, then they're also up to the task of finding an
appropriate third party library.”

To that I say, good luck. If you go out there, you'll find over a dozen
different solutions all with different APIs and varying levels of compatibility
and performance. If we decided only by most-downloaded we'd end up with blist.
So let's try that.

Blist implements a B-tree data type in C with a node size of 128. And I was
happy with it until one day I made this discovery. I'm surprised here because
blist should shuffle 128 pointers while bisect should shuffle 1000
pointers. How can bisect be faster here?

So I went back to the libraries and tried some others. RBtree uses
Red-Black. Banyan has that too and a Splay option. Bintrees has Binary,
Red-Black and AVL. All of those are implemented in C or C++. Then I discovered
a Skip-list implementation that was slower but pure-Python.

All I can say in five minutes is :doc:`Sorted Containers<index>` doesn't use
any of these exactly. It's kind of like a B-tree but only half-heartedly. It
relies entirely on the bisect module. While it's slow to program in Python, the
interpreter is written in C. So if you think of it as programming the
interpreter, you're effectively writing C code. It turns out lists are fast;
trees, not so much.

Listen to what these smart people have to say about it:

* Alex Martelli: Good stuff! ... I like the simple, effective implementation
  idea of splitting the sorted containers into smaller “fragments” to avoid the
  O(N) insertion costs.

* Jeff Knupp: That last part, “fast as C-extensions,” was difficult to
  believe. I would need some sort of performance comparison to be convinced
  this is true. The author includes this in the docs. It is.

* Kevin Samuel, I’m quite amazed, not just by the code quality, but the actual
  amount of work you put at stuff that is not code: documentation,
  benchmarking, implementation explanations.

Lastly, Mark Summerfield makes a short plea: Python’s “batteries included”
standard library seems to have a battery missing. And the argument that “we
never had it before” has worn thin. It is time that Python offered a full range
of collection classes out of the box, including sorted ones.

Ladies and gentlemen, the :doc:`Sorted Containers<index>` library. Thank you.

.. _`Accompanying Slides`: http://bit.ly/socoin5
