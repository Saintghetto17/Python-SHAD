import pytest

from .range import Range


def test_basic() -> None:
    n = 0
    for i in Range(10):
        n += i
    assert n == 45

    n = 0
    for i in Range(0, 10, 2):
        n += i
    assert n == 20


def test_renewable() -> None:
    range_ = Range(3)

    n = 0
    for i in range_:
        n += 1
    assert n == 3

    for i in range_:
        n += 1
    assert n == 6


def test_fast() -> None:
    for i in range(10000):
        assert 500000 in Range(1000000)


def test_repr() -> None:
    assert str(range(10)) == str(Range(10))
    assert str(range(10, 20)) == str(Range(10, 20))
    assert str(range(10, 20, 2)) == str(Range(10, 20, 2))
    assert str(range(10, 20, 1)) == str(Range(10, 20, 1))


def test_len() -> None:
    assert len(range(100)) == len(Range(100))
    assert len(range(3, 33, 7)) == len(Range(3, 33, 7))
    assert len(range(10, 3, -3)) == len(Range(10, 3, -3))
    assert len(range(10, 0, -1)) == len(Range(10, 0, -1))
    assert len(range(10, 0)) == len(Range(10, 0))
    assert len(range(0, 10, -1)) == len(Range(0, 10, -1))


def test_stop() -> None:
    with pytest.raises(StopIteration):
        range_ = iter(Range(3))
        for _ in range(4):
            next(range_)


def test_access() -> None:
    for i in range(4):
        assert range(2, 6)[i] == Range(2, 6)[i]

    for i in range(4):
        assert range(-2, -6, -1)[i] == Range(-2, -6, -1)[i]

    for i in range(4):
        assert range(2, -2, -1)[i] == Range(2, -2, -1)[i]

    for i in range(-5, 0, -1):  # access by negative index
        assert range(5)[i] == Range(5)[i]

    with pytest.raises(IndexError):
        Range(10, 20, 2)[5]

    with pytest.raises(IndexError):
        Range(-10, -20, -2)[5]

    with pytest.raises(IndexError):
        Range(6, -4, 2)[5]


def test_contains() -> None:
    range_ = Range(0, 10, 2)
    assert 4 in range_
    assert 5 not in range_
    assert 12 not in range_
    assert -2 not in range_

    range_ = Range(10, 0, -2)
    assert 4 in range_
    assert 5 not in range_
    assert 12 not in range_
    assert -2 not in range_


def test_negative() -> None:
    assert list(range(3, 0, -1)) == list(Range(3, 0, -1))
    assert list(range(3, -10, -3)) == list(Range(3, -10, -3))
