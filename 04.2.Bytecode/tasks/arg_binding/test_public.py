import sys
from types import FunctionType
from typing import cast

import pytest

# don't use `inspect` pls
sys.modules['inspect'] = None  # type: ignore # noqa

from .arg_binding import (  # noqa: E402
    bind_args,
    ERR_TOO_MANY_POS_ARGS,
    ERR_TOO_MANY_KW_ARGS,
    ERR_MULT_VALUES_FOR_ARG,
    ERR_MISSING_POS_ARGS,
    ERR_MISSING_KWONLY_ARGS,
    ERR_POSONLY_PASSED_AS_KW,
)


def test_no_args() -> None:
    def foo():                  # type: ignore
        pass

    foo = cast(FunctionType, foo)
    assert bind_args(foo) == {}


def test_positional() -> None:
    def foo(a, b, c): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, 1, 2, 3) \
        == dict(a=1, b=2, c=3)
    assert bind_args(foo, 'abc', [1, 2, 3], None) \
        == dict(a='abc', b=[1, 2, 3], c=None)


def test_positional_wrong() -> None:
    def foo(a, b, c): pass      # type: ignore
    foo = cast(FunctionType, foo)

    with pytest.raises(TypeError, match=ERR_MISSING_POS_ARGS):
        bind_args(foo, 1, 2)
    with pytest.raises(TypeError, match=ERR_TOO_MANY_POS_ARGS):
        bind_args(foo, 1, 2, 3, 4)


def test_keyword() -> None:
    def foo(a, b, c): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, a=1, b=2, c=3) \
        == dict(a=1, b=2, c=3)
    assert bind_args(foo, c=None, a='abc', b=[1, 2, 3]) \
        == dict(a='abc', b=[1, 2, 3], c=None)


def test_keyword_wrong() -> None:
    def foo(a, b, c): pass      # type: ignore
    foo = cast(FunctionType, foo)

    with pytest.raises(TypeError, match=ERR_MISSING_POS_ARGS):
        bind_args(foo, a=1, c=3)
    with pytest.raises(TypeError, match=ERR_MULT_VALUES_FOR_ARG):
        bind_args(foo, 1, 2, 3, a=10)
    with pytest.raises(TypeError) as err_info:
        bind_args(foo, a='abc', b=[1, 2, 3], d=123)
    assert err_info.value.args[0] in [ERR_MISSING_POS_ARGS, ERR_TOO_MANY_KW_ARGS]


def test_positional_default() -> None:
    def foo(a, b=2, c=3, d=4): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, 1) == dict(a=1, b=2, c=3, d=4)
    assert bind_args(foo, 'abc', c=10) == dict(a='abc', b=2, c=10, d=4)
    with pytest.raises(TypeError, match=ERR_MISSING_POS_ARGS):
        bind_args(foo, b=2, c=3, d=4)


def test_kwonly() -> None:
    def foo(*, a, b, c): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, a=1, b=2, c=3) \
        == dict(a=1, b=2, c=3)
    assert bind_args(foo, c=None, a='abc', b=[1, 2, 3]) \
        == dict(a='abc', b=[1, 2, 3], c=None)


def test_kwonly_wrong() -> None:
    def foo(*, a, b, c): pass      # type: ignore
    foo = cast(FunctionType, foo)

    with pytest.raises(TypeError, match=ERR_TOO_MANY_POS_ARGS):
        bind_args(foo, 1, 2, 3)
    with pytest.raises(TypeError, match=ERR_MISSING_KWONLY_ARGS):
        bind_args(foo, a=1, b=2)


def test_kwonly_default() -> None:
    def foo(*, a=1, b=2, c=3): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo) == dict(a=1, b=2, c=3)
    assert bind_args(foo, c=None) == dict(a=1, b=2, c=None)
    with pytest.raises(TypeError, match=ERR_TOO_MANY_POS_ARGS):
        bind_args(foo, 100)


def test_posonly() -> None:
    def foo(a, /, b): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, 1, 2) == dict(a=1, b=2)
    assert bind_args(foo, 10, b=20) == dict(a=10, b=20)
    with pytest.raises(TypeError, match=ERR_POSONLY_PASSED_AS_KW):
        bind_args(foo, a=100, b=200)
    with pytest.raises(TypeError, match=ERR_POSONLY_PASSED_AS_KW):
        bind_args(foo, 1, a=10)


def test_posonly_default() -> None:
    def foo(a=1, /, b=2): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo) == dict(a=1, b=2)
    assert bind_args(foo, 10) == dict(a=10, b=2)
    assert bind_args(foo, b=20) == dict(a=1, b=20)
    with pytest.raises(TypeError, match=ERR_POSONLY_PASSED_AS_KW):
        bind_args(foo, a=100)
    with pytest.raises(TypeError, match=ERR_POSONLY_PASSED_AS_KW):
        bind_args(foo, 1, a=10)


def test_varargs() -> None:
    def foo(*wtfargs): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, 1, 'a', None, [1, 2, 3]) \
        == dict(wtfargs=(1, 'a', None, [1, 2, 3]))
    assert bind_args(foo) == dict(wtfargs=())


def test_varkwargs() -> None:
    def foo(**kekwargs): pass      # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, foo=1, bar='spam', baz=['eggs']) \
        == dict(kekwargs=dict(foo=1, bar='spam', baz=['eggs']))
    assert bind_args(foo) == dict(kekwargs={})


def test_posonly_varkwargs() -> None:
    def foo(a, /, **kwargs): pass  # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, 1, a=2) == dict(a=1, kwargs=dict(a=2))


def test_kwonly_varkwargs() -> None:
    def foo(*, d, e, f='default', **kekwargs): pass  # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, d=4, e=5, f=6) \
        == dict(d=4, e=5, f=6, kekwargs={})
    assert bind_args(foo, z=1, d=4, e=5, f=6) \
        == dict(d=4, e=5, f=6, kekwargs={'z': 1})


def test_local_variables_only() -> None:
    def foo():                  # type: ignore
        a_local_variable = 123  # noqa

    foo = cast(FunctionType, foo)
    assert bind_args(foo) == {}


def test_local_variables() -> None:
    def foo(*args):             # type: ignore
        a_local_variable = 123  # noqa

    foo = cast(FunctionType, foo)
    assert bind_args(foo, 1, 2) == dict(args=(1, 2))


def test_multiple_values_args_kwargs() -> None:
    def foo(a, *args, **kwargs): pass  # type: ignore
    foo = cast(FunctionType, foo)
    with pytest.raises(TypeError, match=ERR_MULT_VALUES_FOR_ARG):
        bind_args(foo, 2, a=3)


def test_multiple_values_args_kwargs_default() -> None:
    def foo(a=1, *args, **kwargs): pass  # type: ignore
    foo = cast(FunctionType, foo)
    with pytest.raises(TypeError, match=ERR_MULT_VALUES_FOR_ARG):
        bind_args(foo, 2, a=3)


def test_everything() -> None:
    def foo(a, /, b, c=None, *args, d, e, f='default', **kwargs): pass  # type: ignore
    foo = cast(FunctionType, foo)

    assert bind_args(foo, 1, 2, 3, d=4, e=5, f=6) \
        == dict(a=1, b=2, c=3, args=(), d=4, e=5, f=6, kwargs={})
    assert bind_args(foo, 1, 2, d=4, e=5) \
        == dict(a=1, b=2, c=None, args=(), d=4, e=5, f='default', kwargs={})
    assert bind_args(foo, 1, 2, 3, 4, 5, 6, d=4, e=5, z=100) \
        == dict(a=1, b=2, c=3, args=(4, 5, 6), d=4, e=5, f='default', kwargs={'z': 100})
    with pytest.raises(TypeError, match=ERR_MISSING_KWONLY_ARGS):
        bind_args(foo, 1, 2, 3, 4, 5, 6)
    with pytest.raises(TypeError, match=ERR_MISSING_KWONLY_ARGS):
        bind_args(foo, 1, 2)
    with pytest.raises(TypeError, match=ERR_MISSING_POS_ARGS):
        bind_args(foo, **dict(a=1, b=2, d=4, e=5))
