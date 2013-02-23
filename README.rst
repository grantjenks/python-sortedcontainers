# Sorted Containers

Pure-Python module for sorted container data types.

Currently, only contains an implementation of sorted list.

# TODO

* Slice support for delitem, getitem, setitem
* Audit places where iteration happens manually

# Testing

Currently tested with CPython version 2.7.

# Performance

Planned: benchmark against the popular blist module.

# Goals

## More Containers

* sortedset
* sorteddict

## Better Testing

* CPython versions 2.5.4, 2.6.6, 3.1.4, 3.2.3 and 3.3.0
* http://www.python.org/download/releases/2.5.4/
* http://www.python.org/download/releases/2.6.6/
* http://www.python.org/download/releases/3.1.4/
* http://www.python.org/download/releases/3.2.3/
* http://www.python.org/download/releases/3.3.0/

## Better Performance

* Cython

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

# License

Copyright 2012 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
