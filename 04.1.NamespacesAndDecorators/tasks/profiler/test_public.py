from collections import namedtuple
from datetime import datetime

from .profiler import profiler


@profiler
def ackermann(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    if m > 0 and n == 0:
        return ackermann(m - 1, 1)
    if m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    assert False, 'unreachable'


@profiler
def strange_function(a, b, c=1, d=2):  # type: ignore
    return a.foo + b.bar + c + d


def test_example() -> None:
    start = datetime.now()
    result = ackermann(3, 2)
    delta = datetime.now() - start

    assert ackermann.calls == 541
    assert delta.total_seconds() / 2 <= ackermann.last_time_taken <= delta.total_seconds(), 'Wrong last time taken'
    assert result == 29


def test_profiler_one_call() -> None:
    start = datetime.now()
    result = ackermann(3, 2)
    delta = datetime.now() - start

    assert ackermann.calls == 541
    assert delta.total_seconds() / 2 <= ackermann.last_time_taken <= delta.total_seconds(), 'Wrong last time taken'
    assert result == 29


def test_profiler_many_call() -> None:
    _ = ackermann(0, 1)
    _ = ackermann(3, 2)
    assert ackermann.calls == 541


def test_profiler_strange_akkerman() -> None:
    foo = namedtuple('foo', ['foo', 'bar'])
    expected_result = 10
    result = strange_function(foo(1, 2), foo(1, 2), 3, 4)
    assert result == expected_result


def test_profiler_not_changes_func() -> None:
    @profiler
    def f() -> None:
        """test"""
        pass

    assert f.__name__ == 'f'
    assert f.__doc__ == 'test'
    assert f.__module__ == __name__
