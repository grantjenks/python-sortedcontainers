# Sorted Containers

Sorted container data types: sorted list, sorted set, and sorted dict.

# Features

* Feature-rich
* Performance matters
* Pure-Python
* 100% test coverage
* Stress testing
* Pragmatic design (e.g. use set for sortedset)

# TODO

* Benchmark sortedset
* SortedDict.iloc -> index location (self._list.__getitem__)
* Stress testing
* Test Python 2.6
* Test Python 3.2
* Test Python 3.3
* Documentation
* Parse benchmark results and publish
* Measure memory usage

# Testing

Currently tested with CPython version 2.7.

# Performance

Planned: benchmark against the popular blist module.

# Goals

## More Containers

* priority queue - maybe better term as a "PriorityDict": a map-like object for which iteration depends on the ordering of the values
  - dict for mapping
  - sortedlist of (value, key) tuples for ordering
  - require keys and values to be orderable
  - require values to be hashable

## Better Testing

* CPython versions 2.6, 3.2 and 3.3

## Better Performance

* Cython
* PyPI

# Benchmark

## Routines

### SortedSet

* __and__ (intersection)
* __eq__
* __or__ (union)
* __sub__ (difference)
* __xor__ (symmetric_difference)
* pop
* remove
* update

## Competitors

* https://pypi.python.org/pypi/rbtree
  - c-module
  - rbtree.rbtree is SortedDict
  - rbtree.rbset is SortedSet
* https://pypi.python.org/pypi/blist
  - c and python implementations
  - blist.sortedlist is SortedList
  - blist.sorteddict is SortedDict
  - blist.sortedset is SortedSet
* https://pypi.python.org/pypi/treap
  - depends on cython
  - treap.treap is SortedDict
* https://pypi.python.org/pypi/bintrees
  - had to install from exe on Windows
  - bintrees.FastAVLTree is SortedDict & SortedSet
  - bintrees.FastRBTree is SortedDict & SortedSet
* https://pypi.python.org/pypi/skiplistcollections
  - pure python
  - skiplistcollections.SkipListDict
  - skiplistcollections.SkipListSet

## Not Easily Installable

* http://newcenturycomputers.net/projects/rbtree.html
* https://github.com/pgrafov/python-avl-tree
* https://pypi.python.org/pypi/pyavl
  - Fails to install on Windows

# License

Copyright 2014 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
