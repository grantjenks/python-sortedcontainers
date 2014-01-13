# Sorted Containers

Sorted container data types: sorted list, sorted set, and sorted dict.

# Features

* Feature-rich
* Performance matters
* Pure-Python

# TODO

* Stress testing for sorteddict
* Benchmark sortedlist
* Benchmark sortedset
* Benchmark sorteddict

# Testing

Currently tested with CPython version 2.7.

# Performance

Planned: benchmark against the popular blist module.

# Goals

## More Containers

* priority queue - maybe better term as a "PriorityDict": a map-like object for which iteration depends on the ordering of the values

## Better Testing

* CPython versions 2.6, 3.2 and 3.3

## Better Performance

* Cython
* PyPI

# Alternatives

* http://pypi.python.org/pypi/treap/0.995
  - slow, c-impl
* http://pypi.python.org/pypi/blist/
  - slow, c-impl
* http://pypi.python.org/pypi/rbtree/
  - fast, c-impl
* https://github.com/pgrafov/python-avl-tree
* http://sourceforge.net/projects/pyavl/
  - easy_install failed on Windows, c-impl
* http://newcenturycomputers.net/projects/rbtree.html
  - slow, pure-python
* http://pythonsweetness.tumblr.com/post/45227295342/fast-pypy-compatible-ordered-map-in-89-lines-of-python
  - fast, pure-python

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
