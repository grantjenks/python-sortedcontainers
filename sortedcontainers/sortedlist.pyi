from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload
)

_T = TypeVar("_T")
_SL = TypeVar("_SL", bound=SortedList)
_SKL = TypeVar("_SKL", bound=SortedKeyList)
_Key = Callable[[_T], Any]
_Repr = Callable[[], str]

def recursive_repr(fillvalue: str = ...) -> Callable[[_Repr], _Repr]: ...


class SortedList(MutableSequence[_T]):

    DEFAULT_LOAD_FACTOR: int = ...
    def __init__(self, iterable: Optional[Iterable[_T]] = ..., key: Optional[_Key[_T]] = ...): ...

    # NB: currently mypy does not honour return type, see mypy #3307
    @overload
    def __new__(cls: Type[_SL], iterable: None, key: None) -> _SL: ...
    @overload
    def __new__(cls: Type[_SL], iterable: None, key: _Key[_T]) -> SortedKeyList[_T]: ...
    @overload
    def __new__(cls: Type[_SL], iterable: Iterable[_T], key: None) -> _SL: ...
    @overload
    def __new__(cls, iterable: Iterable[_T], key: _Key[_T]) -> SortedKeyList[_T]: ...

    @property
    def key(self) -> Optional[Callable[[_T], Any]]: ...
    def _reset(self, load: int) -> None: ...
    def clear(self) -> None: ...
    def _clear(self) -> None: ...
    def add(self, value: _T) -> None: ...
    def _expand(self, pos: int) -> None: ...
    def update(self, iterable: Iterable[_T]) -> None: ...
    def _update(self, iterable: Iterable[_T]) -> None:...
    def discard(self, value: _T) -> None: ...
    def remove(self, value: _T) -> None: ...
    def _delete(self, pos: int, idx: int) -> None: ...
    def _loc(self, pos: int, idx: int) -> int: ...
    def _pos(self, idx: int) -> int: ...
    def _build_index(self) -> None: ...
    def __contains__(self, value: Any) -> bool: ...
    def __delitem__(self, index: Union[int, slice]) -> None: ...
    @overload
    def __getitem__(self, index: int) -> _T: ...
    @overload
    def __getitem__(self, index: slice) -> List[_T]: ...
    @overload
    def _getitem(self, index: int) -> _T: ...
    @overload
    def _getitem(self, index: slice) -> List[_T]: ...
    @overload
    def __setitem__(self, index: int, value: _T) -> None: ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __reversed__(self) -> Iterator[_T]: ...
    def __len__(self) -> int: ...
    def reverse(self) -> None: ...
    def islice(
        self, start: Optional[int] = ..., stop: Optional[int] = ..., reverse=bool
    ) -> Iterator[_T]: ...
    def _islice(
        self, min_pos: int, min_idx: int, max_pos: int, max_idx: int, reverse: bool
    ) -> Iterator[_T]: ...
    def irange(
        self,
        minimum: Optional[int] = ...,
        maximum: Optional[int] = ...,
        inclusive: Tuple[bool, bool] = ...,
        reverse: bool = ...,
    ) -> Iterator[_T]: ...
    def bisect_left(self, value: _T) -> int: ...
    def bisect_right(self, value: _T) -> int: ...
    def bisect(self, value: _T) -> int: ...
    def _bisect_right(self, value: _T) -> int: ...
    def count(self, value: _T) -> int: ...
    def copy(self: _SL) -> _SL: ...
    def __copy__(self: _SL) -> _SL: ...
    def append(self, value: _T) -> None: ...
    def extend(self, values: Iterable[_T]) -> None: ...
    def insert(self, index: int, value: _T) -> None: ...
    def pop(self, index: int = -1) -> _T: ...
    def index(self, value: _T, start: Optional[int] = None, stop: Optional[int] = None) -> int: ...
    def __add__(self: _SL, other: Iterable[_T]) -> _SL: ...
    def __radd__(self: _SL, other: Iterable[_T]) -> _SL: ...
    def __iadd__(self: _SL, other: Iterable[_T]) -> _SL: ...
    def __mul__(self: _SL, num: int) -> _SL: ...
    def __rmul__(self: _SL, num: int) -> _SL: ...
    def __imul__(self: _SL, num: int) -> _SL: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __lt__(self, other: Sequence[_T]) -> bool: ...
    def __gt__(self, other: Sequence[_T]) -> bool: ...
    def __le__(self, other: Sequence[_T]) -> bool: ...
    def __ge__(self, other: Sequence[_T]) -> bool: ...
    def __repr__(self) -> str: ...
    def _check(self) -> None: ...

class SortedKeyList(SortedList[_T]):
    def __init__(self, iterable: Optional[Iterable[_T]] = ..., key: _Key[_T] = ...) -> None: ...
    def __new__(cls, iterable: Optional[Iterable[_T]] = ..., key: _Key[_T] = ...) -> SortedKeyList[_T]: ...
    @property
    def key(self) -> Callable[[_T], Any]: ...
    def clear(self) -> None: ...
    def _clear(self) -> None: ...
    def add(self, value: _T) -> None: ...
    def _expand(self, pos: int) -> None: ...
    def update(self, iterable: Iterable[_T]) -> None: ...
    def _update(self, iterable: Iterable[_T]) -> None: ...

    # NB: Must be T to be safely passed to self.func, yet base class imposes Any
    def __contains__(self, value: _T) -> bool: ...  # type: ignore
    def discard(self, value: _T) -> None: ...
    def remove(self, value: _T) -> None: ...
    def _delete(self, pos: int, idx: int) -> None: ...
    def irange(
        self,
        minimum: Optional[int] = ...,
        maximum: Optional[int] = ...,
        inclusive: Tuple[bool, bool] = ...,
        reverse: bool = ...,
    ): ...
    def irange_key(
        self,
        min_key: Optional[Any] = ...,
        max_key: Optional[Any] = ...,
        inclusive: Tuple[bool, bool] = ...,
        reserve: bool = ...,
    ): ...
    def bisect_left(self, value: _T) -> int: ...
    def bisect_right(self, value: _T) -> int: ...
    def bisect(self, value: _T) -> int: ...
    def bisect_key_left(self, key: Any) -> int: ...
    def _bisect_key_left(self, key: Any) -> int: ...
    def bisect_key_right(self, key: Any) -> int: ...
    def _bisect_key_right(self, key: Any) -> int: ...
    def bisect_key(self, key: Any) -> int: ...
    def count(self, value: _T) -> int: ...
    def copy(self: _SKL) -> _SKL: ...
    def __copy__(self: _SKL) -> _SKL: ...
    def index(self, value: _T, start: Optional[int] = ..., stop: Optional[int] = ...) -> int: ...
    def __add__(self: _SKL, other: Iterable[_T]) -> _SKL: ...
    def __radd__(self: _SKL, other: Iterable[_T]) -> _SKL: ...
    def __iadd__(self: _SKL, other: Iterable[_T]) -> _SKL: ...
    def __mul__(self: _SKL, num: int) -> _SKL: ...
    def __rmul__(self: _SKL, num: int) -> _SKL: ...
    def __imul__(self: _SKL, num: int) -> _SKL: ...
    def __repr__(self) -> str: ...
    def _check(self) -> None: ...

SortedListWithKey = SortedKeyList
