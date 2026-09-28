import pytest

from sortedcontainers import SortedSet


@pytest.mark.parametrize('key', [None, int])
def test_failed_add_preserves_membership_and_sorted_index(key):
    values = SortedSet([1, 2, 3], key=key)
    with pytest.raises((TypeError, ValueError)):
        values.add('invalid')
    assert 'invalid' not in values
    assert len(values) == 3
    assert list(values) == [1, 2, 3]
    values._check()
    values.add(4)
    assert values.pop() == 4
    values._check()


def test_failed_add_key_can_be_retried():
    def key(value):
        if fail[0]:
            raise ValueError('cannot calculate key')
        return value

    fail = [False]
    values = SortedSet([1], key=key)
    fail[0] = True
    with pytest.raises(ValueError, match='cannot calculate key'):
        values.add(2)
    fail[0] = False
    values.add(2)
    assert list(values) == [1, 2]
    values._check()


@pytest.mark.parametrize('operation', ['update', 'ior'])
def test_failed_rebuild_update_preserves_membership_and_sorted_index(operation):
    fail = [False]

    def key(value):
        if fail[0] and value >= 10:
            raise ValueError('cannot calculate key')
        return value

    values = SortedSet([1, 2, 3], key=key)
    bisect_left = values.bisect_left
    isdisjoint = values.isdisjoint
    fail[0] = True
    with pytest.raises(ValueError, match='cannot calculate key'):
        if operation == 'update':
            values.update([10, 11, 12, 13])
        else:
            values |= [10, 11, 12, 13]
    assert len(values) == 3
    assert list(values) == [1, 2, 3]
    assert 10 not in values
    values._check()

    fail[0] = False
    values.update([10, 11, 12, 13])
    assert list(values) == [1, 2, 3, 10, 11, 12, 13]
    assert bisect_left(10) == 3
    assert isdisjoint({10}) is False
    values._check()
