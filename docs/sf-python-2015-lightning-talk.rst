SF Python 2015 Lightning Talk
=============================

* `Accompanying Slides`_

Good evening! I'm Grant Jenks. Let's talk about a missing battery.

My journey started here. From collections import sorted
dictionary. Oops. That's an import error. Import sorted list. Import
error. Import sorted set. Import error.

I don't always import sorted types. But when I do, I expect them in the
standard lib.

And why would I expect that? I don't know. I guess PHP and Javascript don't
have 'em either.

But the chorus and the refrain from core developers is: "Look to the PyPI." Ok,
good advice.

Here's what that's like. It's like walking into my daughter's room after she's
dumped all her toys on the floor. Seriously. PyPI has got to work better than
using Google with the site operator.

I love Python because there's one right way to do things. Just give me sorted
types.

I'm not the only one asking. Neil asked this in 2011. And Nick answered. "If a
user is sophisticated enough to realise that the builtin types aren't the right
solution for their problem, then they're also up to the task of finding an
appropriate third party library."

Okay. Fine. But just tell me the right answer. Give me a standard-lib-plus-plus
or something.

I couldn't find the right answer so I built it. Here it is. Sorted
Containers. The right answer is pure-Python. It's Python 2 and Python 3
compatible. It's fast. It's fully-featured. And it's extensively tested with
100% coverage and hours of stress.

Performance is a feature. That means graphs. Lot's of them. Here's the
performance of creating a sorted list from random numbers. I benchmark Sorted
Containers against every worthy competitor I can find.

Here we see it's five to ten times faster than sortedcollection which is in
fact a little recipe Raymond wrote and linked from the Python docs.

Sorted dictionaries have the most competition. And the performance of Sorted
Containers is great. And it's not just initializing that's fast. Every common
method is benchmarked for you.

Here's a quick look at sorted sets and your options. The blist module is kind
of the incumbent. It works great as a specialized list. But please stop using
it for sorted types.

There are also benchmarks across runtimes. When you write pure-Python code, it
really screams on PyPy. Notice where the JIT kicks in around a hundred thousand
list items. The speedup is greater than 10x.

In addition to the typical sequence, mapping, and set apis, there's a number of
bonus methods which are possible because of the sort order constraint.

For example, sorted lists include bisect methods and there's an islice method
that implements slice indexing but returns an iterator.

Sorted dictionaries also support integer indexing. You can lookup the index of
a key or bisect keys in a mapping. There's even an iloc attribute that
functions similarly to Pandas' DataFrames. Also included is an irange method
that iterates ranges of keys.

Likewise, sorted sets fully support positional indexing and lookup.

If you're curious how it works, there's a page with implementation details. The
short answer is two fold: I use bisect a lot and I cheat a little. But never
fear, none of the graphs hide lazy-computations.

I think :doc:`Sorted Containers<index>` is great. But listen to what other
smart people say about it:

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

So, the next time you write a priority queue, or work with time-series data, or
setup an in-memory Sqlite database or send Redis a ZADD command, think of
:doc:`Sorted Containers<index>`.

In Python, we can do better. Happy Holidays.

.. _`Accompanying Slides`: http://bit.ly/soco5sf
