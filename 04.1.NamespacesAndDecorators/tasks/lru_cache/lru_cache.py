import functools
import typing
from collections.abc import Callable
from typing import Any, TypeVar
from collections import OrderedDict

Function = TypeVar('Function', bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """

    def wraps(func: Function) -> Function:

        cash: OrderedDict[tuple[Any, ...], Any] = OrderedDict()
        capacity = max_size
        size = 0

        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            nonlocal size
            nonlocal capacity
            keys_args: tuple[Any, ...] = tuple([*args])
            merged = keys_args
            if merged not in cash.keys():
                if size <= capacity:
                    res = func(*args, **kwargs)
                    cash[merged] = res
                    size = size + 1
                else:
                    res = func(*args, **kwargs)
                    cash[merged] = res
                    keys: list[tuple[Any, ...]] = list(cash.keys())
                    key_first = keys[0]
                    cash.pop(key_first)
                return cash[merged]
            else:
                return cash[merged]

        return typing.cast(Function, wrapper)

    return wraps
