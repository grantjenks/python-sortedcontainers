"""Sorted Array
===============


:doc:`Sorted Containers<index>` is an Apache2 licensed Python sorted
collections library, written in pure-Python, and fast as C-extensions. The
:doc:`introduction<introduction>` is the best way to get started.

Sorted list implementations:

.. currentmodule:: sortedcontainers

* :class:`SortedArray`

"""
# pylint: disable=too-many-lines
from __future__ import print_function
from sys import hexversion

from .sortedlist import SortedList, recursive_repr
from array import array

class SortedArray(SortedList):
    """Sorted array is a sorted mutable sequence.

    Sorted array values are maintained in sorted order.

    Underlying data structure is the standard library array.array
    Enables densly packed lists floats and doubles.
    Enables densly packed lists of integers in CPython.

    Methods for adding values:

    * :func:`SortedArray.add`
    * :func:`SortedArray.update`
    * :func:`SortedArray.__add__`
    * :func:`SortedArray.__iadd__`
    * :func:`SortedArray.__mul__`
    * :func:`SortedArray.__imul__`

    Methods for removing values:

    * :func:`SortedArray.clear`
    * :func:`SortedArray.discard`
    * :func:`SortedArray.remove`
    * :func:`SortedArray.pop`
    * :func:`SortedArray.__delitem__`

    Methods for looking up values:

    * :func:`SortedArray.bisect_left`
    * :func:`SortedArray.bisect_right`
    * :func:`SortedArray.count`
    * :func:`SortedArray.index`
    * :func:`SortedArray.__contains__`
    * :func:`SortedArray.__getitem__`

    Methods for iterating values:

    * :func:`SortedArray.irange`
    * :func:`SortedArray.islice`
    * :func:`SortedArray.__iter__`
    * :func:`SortedArray.__reversed__`

    Methods for miscellany:

    * :func:`SortedArray.copy`
    * :func:`SortedArray.__len__`
    * :func:`SortedArray.__repr__`
    * :func:`SortedArray._check`
    * :func:`SortedArray._reset`

    Sorted lists use lexicographical ordering semantics when compared to other
    sequences.

    Some methods of mutable sequences are not supported and will raise
    not-implemented error.

    """
    DEFAULT_LOAD_FACTOR = 1000


    def __init__(self, typecode, initializer=None):
        """Initialize sorted list instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted list.

        Runtime complexity: `O(n*log(n))`

        >>> sl = SortedArray('i')
        >>> sl
        SortedArray('i', [])
        >>> sl = SortedArray('i', [3, 1, 2, 5, 4])
        >>> sl
        SortedArray('i', [1, 2, 3, 4, 5])

        :param typecode: type code for the array, as in the array.array standard library class (required)
        :param iterable: initial values (optional)

        """
        self._typecode = typecode
        if hexversion >= 0x03000000:
            super().__init__(iterable=initializer, key=None)
        else:
            super(SortedArray, self).__init__(iterable=initializer, key=None)


    def __new__(cls, typecode, initializer=None):
        # pylint: disable=unused-argument
        if hexversion >= 0x03000000:
            return super().__new__(cls, iterable=initializer, key=None)
        else:
            return super(SortedArray, cls).__new__(cls, iterable=initializer, key=None)


    def _new_list(self):
        _typecode = self._typecode
        return array(_typecode)


    def _sort_in_place(self, _list):
        # array.array does not support sort in place
        sorted_list = sorted(_list)
        del _list[:]
        _list.extend(sorted_list)


    @recursive_repr()
    def __repr__(self):
        """Return string representation of sorted array.

        ``sa.__repr__()`` <==> ``repr(sa)``

        :return: string representation

        >>> sa = SortedArray('i',[5,4,3])
        >>> sa
        SortedArray('i', [3, 4, 5])
        """
        class_name = type(self).__name__
        _typecode = self._typecode
        return "{0}('{1}', {2!r})".format(class_name, _typecode, list(self))
