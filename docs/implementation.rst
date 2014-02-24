Implementation Details
======================

// bisect insort is fast
// a little similar to "compact dynamic array"
// not tree based
// index lookup done with cumulative sum list of lengths
// why it works: processors are really fast with arrays
// 'load' value
// _lists, _maxes, _index
