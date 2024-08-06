import dataclasses
import types
from textwrap import dedent

import pytest

from .codeops import count_operations


@dataclasses.dataclass
class Case:
    source_code: str
    op_counts: dict[str, int]

    @property
    def code(self) -> types.CodeType:
        dedent_source_code = dedent(self.source_code)
        return compile(dedent_source_code, '<string>', 'exec')


TEST_CASES = [
    Case(
        source_code="""
            a = 1
            b = 2
            a += b
            print(a)
        """,
        op_counts={
            'BINARY_OP': 1,
            'CALL': 1,
            'LOAD_CONST': 3,
            'LOAD_NAME': 4,
            'POP_TOP': 1,
            'PRECALL': 1,
            'PUSH_NULL': 1,
            'RESUME': 1,
            'RETURN_VALUE': 1,
            'STORE_NAME': 3,
        }
    ),
    Case(
        source_code="""
            def f():
                a = 1
            f()
        """,
        op_counts={
            'CALL': 1,
            'LOAD_CONST': 4,
            'LOAD_NAME': 1,
            'MAKE_FUNCTION': 1,
            'POP_TOP': 1,
            'PRECALL': 1,
            'PUSH_NULL': 1,
            'RESUME': 2,
            'RETURN_VALUE': 2,
            'STORE_FAST': 1,
            'STORE_NAME': 1,
        }
    ),
    Case(
        source_code="""
            def f():
                a = 1
            print(f())
        """,
        op_counts={
            'CALL': 2,
            'LOAD_CONST': 4,
            'LOAD_NAME': 2,
            'MAKE_FUNCTION': 1,
            'POP_TOP': 1,
            'PRECALL': 2,
            'PUSH_NULL': 2,
            'RESUME': 2,
            'RETURN_VALUE': 2,
            'STORE_FAST': 1,
            'STORE_NAME': 1,
        }
    ),
    Case(
        source_code="""
            def foo(x):
                return x**2
            def bar(x):
                return x*2
            print(bar(foo(10)))
        """,
        op_counts={
            'BINARY_OP': 2,
            'CALL': 3,
            'LOAD_CONST': 6,
            'LOAD_FAST': 2,
            'LOAD_NAME': 3,
            'MAKE_FUNCTION': 2,
            'POP_TOP': 1,
            'PRECALL': 3,
            'PUSH_NULL': 3,
            'RESUME': 3,
            'RETURN_VALUE': 3,
            'STORE_NAME': 2,
        }
    ),
    Case(
        source_code="""
            def foo():
                def bar():
                    def baz():
                        return 1
                    return baz
                return bar
        """,
        op_counts={
            'LOAD_CONST': 5,
            'LOAD_FAST': 2,
            'MAKE_FUNCTION': 3,
            'RESUME': 4,
            'RETURN_VALUE': 4,
            'STORE_FAST': 2,
            'STORE_NAME': 1,
        }
    ),
    Case(
        source_code="""
            def f():
                a = 1
            f()
            f()
            f()
        """,
        op_counts={
            'CALL': 3,
            'LOAD_CONST': 4,
            'LOAD_NAME': 3,
            'MAKE_FUNCTION': 1,
            'POP_TOP': 3,
            'PRECALL': 3,
            'PUSH_NULL': 3,
            'RESUME': 2,
            'RETURN_VALUE': 2,
            'STORE_FAST': 1,
            'STORE_NAME': 1,
        },
    ),
]


@pytest.mark.parametrize('t', TEST_CASES)
def test_count_operations(t: Case) -> None:
    assert count_operations(t.code) == t.op_counts
