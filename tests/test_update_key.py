from bisect import bisect_right
from random import Random

import pytest

from sortedcontainers import SortedKeyList, SortedList


@pytest.mark.parametrize('load', [4, 7, 1000])
@pytest.mark.parametrize('old, new', [(0, 99), (29, -1), (2, 9.5), (10, 1.5), (7, 7.5)])
def test_repositions_by_index_and_preserves_identity(load, old, new):
    values = [[i, i] for i in range(30)]
    skl = SortedKeyList(values, key=lambda value: value[0])
    skl._reset(load)
    skl._build_index()
    changed = skl[old]
    changed[0] = new
    position = skl.update_key(old)
    assert skl[position] is changed
    assert list(skl) == sorted(values, key=lambda value: value[0])
    assert len(skl) == 30
    skl._check()


def test_unchanged_position_does_not_remove_insert_or_rebalance():
    values = [[i] for i in range(30)]
    calls = []
    skl = SortedKeyList(values, key=lambda value: calls.append(value) or value[0])
    skl._reset(4)
    skl._build_index()
    blocks = [id(block) for block in skl._lists]
    tree = list(skl._index)
    calls.clear()
    values[7][0] = 7.5
    assert skl.update_key(7) == 7
    assert [id(block) for block in skl._lists] == blocks
    assert skl._index == tree
    assert calls == [values[7]]
    skl._check()
    assert skl.bisect_key_right(7.5) == 8


@pytest.mark.parametrize('old, new', [(1, 5.5), (5, 0.5)])
def test_move_inside_block_keeps_block_sizes_and_index(old, new):
    values = [[i] for i in range(24)]
    skl = SortedKeyList(values, key=lambda value: value[0])
    skl._reset(8)
    skl._build_index()
    blocks = [id(block) for block in skl._lists]
    lengths = list(map(len, skl._lists))
    tree = list(skl._index)
    values[old][0] = new
    new_index = skl.update_key(old)
    assert skl[new_index] is values[old]
    assert list(skl) == sorted(values, key=lambda value: value[0])
    assert [id(block) for block in skl._lists] == blocks
    assert list(map(len, skl._lists)) == lengths
    assert skl._index == tree
    skl._check()


def test_negative_index_and_keyed_sorted_list_factory():
    values = [[1], [2], [3]]
    skl = SortedList(values, key=lambda value: value[0])
    values[-1][0] = 0
    assert skl.update_key(-1) == 0
    assert skl[0] is values[-1]
    skl._check()


def test_singleton():
    value = [1]
    skl = SortedKeyList([value], key=lambda item: item[0])
    value[0] = -5
    assert skl.update_key(-1) == 0
    assert skl.bisect_key_left(-5) == 0
    skl._check()


def test_equal_keys_keep_position_when_possible_and_append_after_move():
    values = [[0, 'moving'], [1, 'a'], [1, 'b'], [2, 'c']]
    skl = SortedKeyList(values, key=lambda value: value[0])
    assert skl.update_key(2) == 2
    values[0][0] = 2
    assert skl.update_key(0) == 3
    assert [value[1] for value in skl] == ['a', 'b', 'c', 'moving']
    skl._check()


@pytest.mark.parametrize('index', [0, -1, 20, -20])
def test_empty_index_error_does_not_call_key(index):
    skl = SortedKeyList(key=lambda value: pytest.fail('unexpected key call'))
    with pytest.raises(IndexError):
        skl.update_key(index)


@pytest.mark.parametrize('index', [3, -4, 1.0, slice(1), '1'])
def test_invalid_index_leaves_data_unchanged(index):
    skl = SortedKeyList([1, 2, 3])
    with pytest.raises((IndexError, TypeError)):
        skl.update_key(index)
    assert list(skl) == [1, 2, 3]
    skl._check()


def test_index_protocol():
    class Position:
        def __index__(self):
            return 1

    skl = SortedKeyList([1, 2, 3])
    assert skl.update_key(Position()) == 1


def test_key_error_does_not_change_cached_keys_or_items():
    value = [1]
    skl = SortedKeyList([value, [2]], key=lambda item: item[0])
    value.clear()
    with pytest.raises(IndexError):
        skl.update_key(0)
    assert skl[0] is value
    assert skl._keys == [[1, 2]]
    assert len(skl) == 2


def test_comparison_error_does_not_change_cached_keys_or_items():
    values = [[1], [2]]
    skl = SortedKeyList(values, key=lambda value: value[0])
    values[0][0] = object()
    with pytest.raises(TypeError):
        skl.update_key(0)
    assert skl[0] is values[0]
    assert skl._keys == [[1, 2]]


def test_equal_values_are_identified_by_occurrence_not_equality():
    class Value:
        def __init__(self, key):
            self.key = key

        def __eq__(self, other):
            return isinstance(other, Value)

    values = [Value(i) for i in range(12)]
    skl = SortedKeyList(values, key=lambda value: value.key)
    skl._reset(4)
    values[3].key = 99
    assert skl.update_key(3) == 11
    assert list(map(id, skl)) == list(map(id, values[:3] + values[4:] + values[3:4]))
    skl._check()


@pytest.mark.parametrize('load', [4, 5, 8, 32])
def test_random_updates_match_reference_with_merges_splits_and_duplicate_keys(load):
    random = Random(181)
    expected = [[i % 13, i] for i in range(160)]
    expected.sort(key=lambda value: value[0])
    skl = SortedKeyList(expected, key=lambda value: value[0])
    skl._reset(load)
    for _ in range(1500):
        old = random.randrange(len(expected))
        value = expected[old]
        value[0] = random.randrange(-100, 100)
        ordered = (old == 0 or expected[old - 1][0] <= value[0]) and (
            old == len(expected) - 1 or value[0] <= expected[old + 1][0]
        )
        new = old
        if not ordered:
            expected.pop(old)
            new = bisect_right([item[0] for item in expected], value[0])
            expected.insert(new, value)
        actual = skl.update_key(old if random.randrange(2) else old - len(skl))
        assert actual == new
        assert [id(item) for item in skl] == [id(item) for item in expected]
        assert skl[actual] is value
        assert skl.bisect_key_left(value[0]) <= actual < skl.bisect_key_right(value[0])
        skl._check()
