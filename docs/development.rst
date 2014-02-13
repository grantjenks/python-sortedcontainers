Developing and Contributing
===========================

- Development page (discuss improvements)
  - priority dict: a map-like object for which iteration depends on the ordering of the values
    - dict for mapping
    - sortedlist of (value, key) tuples for ordering
    - require keys and values to be orderable
    - require values to be hashable
  - test/benchmark with cython
  - test/benchmark with PyPI
  - better compatibility with blist
    - add "key" option
