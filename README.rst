Sorted Containers
=================

Sorted container data types: sorted list, sorted set, and sorted dict.

# TODO

- Documentation (include plots)
  - Add Abstract Base Classes:
    SortedList: MutableSequence
    SortedDict: MutableMapping
    SortedSet: MutableSet
    KeysView: KeysView, Set, Sequence
    ValuesView: ValuesView, Sequence
    ItemsView: ItemsView, Set, Sequence
  - sorteddict at KeysView; needs cross-ref
  - sortedset review
  - Fix warnings
  - README
- URL todos: http://todo
- document every function/class in source
- add analytics
- deploy to pypi
  - Testing: 2.6, 2.7, 3.2, 3.3
  - Coverage
- publish online: grantjenks.com/docs/sortedcontainers/...
- publish portfolio page
  - Blurb of thanks on project page in blog
    - Add that if K Reitz is known for taking complex APIs and making them
      simple then maybe someday I can be known for making slow APIs into
      fast ones.
- publish docs
- promote
  - email Armin Ronacher
  - email K Reitz
  - email John Cook (The Endeavor)
    - ask for help with big-O analysis

License
-------

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
