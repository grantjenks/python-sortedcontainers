import pytest

from sortedcontainers import SortedSet


@pytest.mark.parametrize('key', [None, int])
@pytest.mark.parametrize('operation', ['method', 'ixor'])
def test_failed_symmetric_difference_preserves_membership_and_index(key, operation):
    values = SortedSet([1, 2, 3], key=key)
    values._reset(7)
    bisect_left = values.bisect_left
    isdisjoint = values.isdisjoint
    incoming = iter([2, 4, 'invalid'])

    with pytest.raises((TypeError, ValueError)):
        if operation == 'method':
            values.symmetric_difference_update(incoming)
        else:
            values ^= incoming

    assert list(values) == [1, 2, 3]
    assert len(values) == 3
    assert 'invalid' not in values
    assert bisect_left(2) == 1
    assert isdisjoint([4])
    values._check()

    assert values.symmetric_difference_update(iter([2, 4])) is values
    assert list(values) == [1, 3, 4]
    assert bisect_left(4) == 2
    assert not isdisjoint([4])
    assert values._list._load == 7
    values._check()
