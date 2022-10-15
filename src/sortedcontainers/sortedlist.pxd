import cython


cdef class SortedList:
    cdef int _len
    cdef int _load
    cdef list _lists
    cdef list _maxes
    cdef list _index
    cdef int _offset

    @cython.locals(pos=int)
    cpdef add(self, value)

    @cython.locals(pos=int, _load=int, _lists_pos=list, child=int)
    cpdef _expand(self, pos)

    @cython.locals(pos=int, idx=int)
    cpdef discard(self, value)

    @cython.locals(pos=int, idx=int)
    cpdef remove(self, value)

    @cython.locals(pos=int, idx=int, _lists_pos=list, child=int)
    cpdef _delete(self, pos, idx)

    @cython.locals(pos=int, idx=int, total=int, index_pos_1=int)
    cpdef _loc(self, pos, idx)

    @cython.locals(
        idx=int,
        _lists_1=list,
        last_len=int,
        pos=int,
        child=int,
        index_child=int,
    )
    cpdef _pos(self, idx)

    @cython.locals(
        row0=list,
        head=int,
        tail=int,
        row1=list,
        size=int,
        tree=list,
        row=list,
    )
    cpdef _build_index(self)

    @cython.locals(pos=int, idx=int)
    cpdef bisect_left(self, value)

    @cython.locals(pos=int, idx=int)
    cpdef bisect_right(self, value)

    cpdef _islice(self, min_pos, min_idx, max_pos, max_idx, reverse)

    cpdef count(self, value)

    cpdef insert(self, index, value)
