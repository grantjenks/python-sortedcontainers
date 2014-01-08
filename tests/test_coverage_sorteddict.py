# -*- coding: utf-8 -*-

import random, string
from context import sortedcontainers
from sortedcontainers import SortedDict
from nose.tools import raises

def test_init():
    temp = SortedDict()
    temp._check()

def test_init_args():
    temp = SortedDict([('a', 1), ('b', 2)])
    assert len(temp) == 2
    assert temp['a'] == 1
    assert temp['b'] == 2
    temp._check()

def test_init_kwargs():
    temp = SortedDict(a=1, b=2)
    assert len(temp) == 2
    assert temp['a'] == 1
    assert temp['b'] == 2
    temp._check()

def test_clear():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert len(temp) == 26
    assert temp.items() == mapping
    temp.clear()
    assert len(temp) == 0

def test_contains():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all((val in temp) for val in string.ascii_lowercase)

def test_delitem():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    del temp['a']
    temp._check()

def test_getitem():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all((temp[val] == pos) for pos, val in enumerate(string.ascii_lowercase))

def test_eq():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp1 = SortedDict(mapping)
    temp2 = SortedDict(mapping)
    assert temp1 == temp2

def test_iter():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert all(lhs == rhs for lhs, rhs in zip(temp, string.ascii_lowercase))

def test_len():
    mapping = [(val, pos) for pos, val in enumerate(string.ascii_lowercase)]
    temp = SortedDict(mapping)
    assert len(temp) == 26

def test_setitem():
    temp = SortedDict()

    for pos, key in enumerate(string.ascii_lowercase):
        temp[key] = pos
        temp._check()

    assert len(temp) == 26

    for pos, key in enumerate(string.ascii_lowercase):
        temp[key] = pos
        temp._check()

    assert len(temp) == 26

if __name__ == '__main__':
    import nose
    nose.main()
