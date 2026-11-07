"""Range deletion preserves mapping, ordering, and block invariants."""

from itertools import product
from operator import neg
from random import Random

import pytest

from sortedcontainers import SortedDict


def decade(value):
    return value // 10


def selected(value, minimum, maximum, inclusive, key):
    key = key or (lambda item: item)
    value = key(value)
    if minimum is not None:
        lower = key(minimum)
        if value < lower or (value == lower and not inclusive[0]):
            return False
    if maximum is not None:
        upper = key(maximum)
        if value > upper or (value == upper and not inclusive[1]):
            return False
    return True


@pytest.mark.parametrize('key', [None, neg, decade])
@pytest.mark.parametrize('inclusive', list(product((False, True), repeat=2)))
def test_range_del_bounds_and_views(key, inclusive):
    for minimum, maximum in product((None, -1, 0, 10, 19, 20, 40), repeat=2):
        mapping = SortedDict(key, ((value, object()) for value in range(30)))
        mapping._reset(4)
        before = list(mapping.items())
        expected = [
            (value, item)
            for value, item in before
            if not selected(value, minimum, maximum, inclusive, key)
        ]
        keys, items, values = mapping.keys(), mapping.items(), mapping.values()

        assert mapping.range_del(minimum, maximum, inclusive) is None

        assert list(items) == expected
        assert list(keys) == [value for value, item in expected]
        assert list(values) == [item for value, item in expected]
        assert dict(mapping) == dict(expected)
        mapping._check()


@pytest.mark.parametrize('key', [None, neg, decade])
def test_range_del_empty(key):
    mapping = SortedDict(key)
    assert mapping.range_del() is None
    assert mapping.range_del(1, 9) is None
    assert not mapping
    mapping._check()


@pytest.mark.parametrize('key', [None, neg, decade])
@pytest.mark.parametrize('load', [4, 5, 8, 25])
def test_range_del_mutations(key, load):
    rng = Random(180)
    mapping = SortedDict(key, ((value, value) for value in range(100)))
    mapping._reset(load)
    model = dict(mapping)
    for step in range(300):
        if step % 3:
            for _ in range(rng.randrange(1, 30)):
                value = rng.randrange(-100, 100)
                mapping[value] = step
                model[value] = step
        else:
            minimum = rng.choice([None, rng.randrange(-120, 120)])
            maximum = rng.choice([None, rng.randrange(-120, 120)])
            inclusive = (rng.choice([True, False]), rng.choice([True, False]))
            model = {
                value: item
                for value, item in model.items()
                if not selected(value, minimum, maximum, inclusive, key)
            }
            mapping.range_del(minimum, maximum, inclusive)

        assert dict(mapping) == model
        expected = sorted(model, key=key)
        assert list(mapping) == expected
        mapping._check()
        if mapping:
            # Exercise rebuilding and later invalidation of the index cache.
            assert mapping.peekitem(len(mapping) // 2)[0] == expected[len(mapping) // 2]


@pytest.mark.parametrize('key', [None, neg])
def test_range_del_preserves_empty_range_index(key):
    mapping = SortedDict(key, ((value, value) for value in range(100)))
    mapping._reset(4)
    mapping.peekitem(51)
    index = mapping._list._index
    original = index[:]
    assert original

    mapping.range_del(40, 40, inclusive=(False, False))
    assert mapping._list._index is index
    assert index == original
    mapping._check()

    lower, upper = (60, 40) if key is neg else (40, 60)
    mapping.range_del(lower, upper)
    assert not index
    assert mapping.peekitem(20)[0] == list(mapping)[20]
    mapping._check()


@pytest.mark.parametrize('key', [None, neg, decade])
def test_range_del_empty_gaps_preserve_block_layout_and_index(key):
    mapping = SortedDict(key, ((value * 10, value) for value in range(100)))
    mapping._reset(4)
    mapping.peekitem(51)
    index = mapping._list._index[:]
    blocks = mapping._list._lists[:]
    before = list(mapping.items())
    for position in range(len(blocks) - 1):
        lower, upper = blocks[position][-1], blocks[position + 1][0]
        mapping.range_del(lower, upper, (False, False))
        assert list(mapping.items()) == before
        assert mapping._list._index == index
        assert all(
            current is previous
            for current, previous in zip(mapping._list._lists, blocks)
        )
    mapping._check()


@pytest.mark.parametrize('key', [None, neg, decade])
def test_range_del_avoids_per_item_search_and_index(key, monkeypatch):
    mapping = SortedDict(key, ((value, value) for value in range(1000)))
    mapping._reset(8)

    def unexpected(*args, **kwargs):
        pytest.fail('range deletion used positional or per-item deletion')

    for name in ('_build_index', '_loc', '_pos', '_delete', 'remove'):
        monkeypatch.setattr(mapping._list, name, unexpected)
    monkeypatch.setattr(mapping, '_list_remove', unexpected)
    lower, upper = (700, 200) if key is neg else (200, 700)
    mapping.range_del(lower, upper)
    assert len(mapping) == sum(
        not selected(value, lower, upper, (True, True), key) for value in range(1000)
    )
    mapping._check()


def test_range_del_uses_cached_sort_keys_and_retains_unaffected_blocks():
    calls = []

    def key(value):
        calls.append(value)
        return value // 10

    mapping = SortedDict(key, ((value, object()) for value in range(1000)))
    mapping._reset(8)
    first_values = mapping._list._lists[0]
    first_keys = mapping._list._keys[0]
    last_values = mapping._list._lists[-1]
    last_keys = mapping._list._keys[-1]
    survivors = {value: mapping[value] for value in (0, 100, 800, 999)}
    calls.clear()

    mapping.range_del(210, 610)

    assert calls == [210, 610]
    assert mapping._list._lists[0] is first_values
    assert mapping._list._keys[0] is first_keys
    assert mapping._list._lists[-1] is last_values
    assert mapping._list._keys[-1] is last_keys
    assert all(mapping[value] is item for value, item in survivors.items())
    mapping._check()


def test_range_del_comparison_failure_does_not_mutate():
    mapping = SortedDict((value, value) for value in range(100))
    mapping._reset(4)
    mapping.peekitem(51)
    before = list(mapping.items())
    blocks = [block[:] for block in mapping._list._lists]
    index = mapping._list._index[:]

    with pytest.raises(TypeError):
        mapping.range_del(20, 'incomparable')

    assert list(mapping.items()) == before
    assert mapping._list._lists == blocks
    assert mapping._list._index == index
    mapping._check()


def test_range_del_key_failure_does_not_mutate():
    def key(value):
        if value == 'failure':
            raise ValueError('invalid bound')
        return -value

    mapping = SortedDict(key, ((value, value) for value in range(100)))
    mapping._reset(4)
    before = list(mapping.items())
    blocks = [block[:] for block in mapping._list._keys]

    with pytest.raises(ValueError, match='invalid bound'):
        mapping.range_del(80, 'failure')

    assert list(mapping.items()) == before
    assert mapping._list._keys == blocks
    mapping._check()


def test_range_del_unordered_keys_and_cached_methods():
    class Key:
        def __init__(self, rank):
            self.rank = rank

    keys = [Key(rank) for rank in range(40)]
    mapping = SortedDict(lambda value: value.rank // 5, ((key, key) for key in keys))
    mapping._reset(4)
    irange = mapping.irange
    bisect_left = mapping.bisect_left
    minimum, maximum = Key(10), Key(20)
    mapping.range_del(minimum, maximum)
    assert list(mapping) == keys[:10] + keys[25:]
    assert list(irange()) == list(mapping)
    assert bisect_left(Key(30)) == 15

    new = Key(11)
    mapping[new] = new
    assert list(irange(Key(10), Key(14))) == [new]
    assert mapping.popitem(0) == (keys[0], keys[0])
    assert mapping.popitem() == (keys[-1], keys[-1])
    mapping._check()


@pytest.mark.parametrize('key', [None, neg, decade])
def test_range_del_block_boundaries(key):
    for size in (1, 5, 17, 31, 48):
        for start in range(size):
            for stop in range(start + 1, size + 1):
                mapping = SortedDict(key, ((value, value) for value in range(size)))
                mapping._reset(4)
                ordered = list(mapping)
                lower, upper = ordered[start], ordered[stop - 1]
                expected = [
                    value
                    for value in ordered
                    if not selected(value, lower, upper, (True, True), key)
                ]
                mapping.range_del(lower, upper)
                assert list(mapping) == expected
                mapping._check()
