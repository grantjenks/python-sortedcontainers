from operator import delitem, getitem

import pytest

from sortedcontainers import SortedDict, SortedList, SortedSet


class Index:
    def __init__(self, value):
        self.value = value
        self.calls = 0

    def __index__(self):
        self.calls += 1
        return self.value


class IntOnly:
    def __int__(self):
        return 0


def pop_at(values, index):
    return values.pop(index)


@pytest.mark.parametrize('key', [None, abs])
@pytest.mark.parametrize('operation', [getitem, delitem, pop_at])
@pytest.mark.parametrize('position', [0, 1, 15, 29, -1, -15, -30])
def test_scalar_index_protocol(key, operation, position):
    expected = list(range(30))
    values = SortedList(expected, key=key)
    values._reset(4)
    index = Index(position)

    assert operation(values, index) == operation(expected, position)
    assert index.calls == 1
    assert list(values) == expected
    values._check()


@pytest.mark.parametrize('key', [None, abs])
@pytest.mark.parametrize('operation', [getitem, delitem, pop_at])
@pytest.mark.parametrize('size', [0, 30])
@pytest.mark.parametrize('index', [0.0, -1.0, 1.0, IntOnly()])
def test_invalid_scalar_indices_do_not_modify_list(key, operation, size, index):
    values = SortedList(range(size), key=key)
    values._reset(4)
    with pytest.raises(TypeError):
        operation(values, index)
    assert list(values) == list(range(size))
    values._check()


@pytest.mark.parametrize('key', [None, abs])
@pytest.mark.parametrize('operation', [getitem, delitem, pop_at])
@pytest.mark.parametrize('size', [0, 30])
@pytest.mark.parametrize('position', [30, -31, 10**100])
def test_index_protocol_out_of_range(key, operation, size, position):
    values = SortedList(range(size), key=key)
    index = Index(position)
    with pytest.raises(IndexError):
        operation(values, index)
    assert index.calls == 1
    assert list(values) == list(range(size))
    values._check()


@pytest.mark.parametrize('operation', [getitem, delitem, pop_at])
@pytest.mark.parametrize('index', [False, True])
def test_boolean_indices(operation, index):
    expected = [1, 2, 3]
    values = SortedList(expected)
    assert operation(values, index) == operation(expected, index)
    assert list(values) == expected
    values._check()


def test_sorted_set_deletion_converts_index_once():
    values = SortedSet(range(5))
    index = Index(2)
    del values[index]
    assert index.calls == 1
    assert list(values) == [0, 1, 3, 4]
    assert 2 not in values
    values._check()


def test_sorted_dict_positional_operations():
    values = SortedDict({1: 'a', 2: 'b', 3: 'c'})
    assert values.peekitem(Index(0)) == (1, 'a')
    assert values.keys()[Index(1)] == 2
    assert values.items()[Index(1)] == (2, 'b')
    assert values.values()[Index(1)] == 'b'
    assert values.popitem(Index(-1)) == (3, 'c')
    del values.keys()[Index(0)]
    assert list(values.items()) == [(2, 'b')]
    values._check()
