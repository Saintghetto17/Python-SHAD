from typing import Any, TypeVar

from _pytest.capture import CaptureFixture  # typing

from .lru_cache import cache


@cache(20)
def binomial(n: int, k: int) -> int:
    if k > n:
        return 0
    if k == 0:
        return 1
    return binomial(n - 1, k) + binomial(n - 1, k - 1)


@cache(2048)
def ackermann(m: int, n: int) -> int:
    print(f'Calculating for {m} and {n}...')
    if m == 0:
        return n + 1
    if m > 0 and n == 0:
        return ackermann(m - 1, 1)
    if m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    assert False, 'unreachable'


@cache(1)
def join(args: tuple[Any, ...] | Any) -> tuple[Any, ...]:
    result: tuple[Any, ...] = tuple()
    for arg in args:
        if isinstance(arg, tuple):
            result += join(arg)
        else:
            result += (arg,)
    return result


def test_cache_not_changes_func() -> None:
    T = TypeVar('T')

    @cache(1)
    def func(a: T) -> T:
        """test doc"""
        return a

    assert func.__name__ == 'func'
    assert func.__doc__ == 'test doc'
    assert func.__module__ == __name__


def test_binomial() -> None:
    result = sum(binomial(30, i) for i in range(31))
    assert result == 2 ** 30


def test_ackermann(capsys: CaptureFixture[str]) -> None:
    result = ackermann(3, 7)
    assert result == 1021
    assert capsys.readouterr().out.count('\n') == 2558


def test_join_lists() -> None:
    result = join(((1, 2, 3), 1, (1, 2, 3, 4, ((1, 2), 2, 3))))
    assert result == (1, 2, 3, 1, 1, 2, 3, 4, 1, 2, 2, 3)


def test_max_cache_size() -> None:
    calls_count = 0
    cache_size = 8

    @cache(cache_size)
    def simple_id(i: int) -> int:
        nonlocal calls_count
        calls_count += 1
        return i

    args = tuple(range(cache_size))
    result = tuple(map(simple_id, args))
    assert result == args
    assert calls_count == cache_size

    args = tuple(range(cache_size, cache_size * 2))
    result = tuple(map(simple_id, args))
    assert result == args
    assert calls_count == cache_size * 2

    args = tuple(range(cache_size))
    result = tuple(map(simple_id, args))
    assert result == args
    assert calls_count == cache_size * 3
