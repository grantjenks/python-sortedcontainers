import cython

cdef class SortedList:
    cdef int _len
    cdef int _load
    cdef list _lists
    cdef list _maxes
    cdef list _index
    cdef int _offset

    @cython.locals(pos=int, idx=int)
    cpdef bisect_right(self, value)

    @cython.locals(pos=int, idx=int, total=int)
    cdef _loc(self, pos, idx)

    @cython.locals(row0=list, head=int, tail=int, row1=list, size=int, tree=list, row=list)
    cdef _build_index(self)
