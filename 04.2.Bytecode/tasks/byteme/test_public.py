import dataclasses
import dis
import io
from typing import Any, Callable
import sys

import pytest

from . import byteme


@dataclasses.dataclass
class Case:
    func: Callable[..., Any]
    expected_dis_out: str

    def __str__(self) -> str:
        return self.func.__name__


TEST_CASES = [
    Case(
        func=byteme.f0,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               0 (None)
   4 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f1,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               1 (0)
   4 STORE_FAST               0 (a)
   6 LOAD_FAST                0 (a)
   8 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f2,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               1 (0)
   4 STORE_FAST               0 (a)
   6 LOAD_GLOBAL              1 (NULL + print)
  18 LOAD_FAST                0 (a)
  20 PRECALL                  1
  24 CALL                     1
  34 POP_TOP
  36 LOAD_CONST               0 (None)
  38 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f3,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               1 (0)
   4 STORE_FAST               0 (a)
   6 LOAD_FAST                0 (a)
   8 LOAD_CONST               2 (1)
  10 BINARY_OP               13 (+=)
  14 STORE_FAST               0 (a)
  16 LOAD_GLOBAL              1 (NULL + print)
  28 LOAD_FAST                0 (a)
  30 PRECALL                  1
  34 CALL                     1
  44 POP_TOP
  46 LOAD_CONST               0 (None)
  48 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f4,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_GLOBAL              1 (NULL + range)
  14 LOAD_CONST               1 (10)
  16 PRECALL                  1
  20 CALL                     1
  30 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f5,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_GLOBAL              1 (NULL + range)
  14 LOAD_CONST               1 (10)
  16 PRECALL                  1
  20 CALL                     1
  30 GET_ITER
  32 FOR_ITER                17 (to 68)
  34 STORE_FAST               0 (i)
  36 LOAD_GLOBAL              3 (NULL + print)
  48 LOAD_FAST                0 (i)
  50 PRECALL                  1
  54 CALL                     1
  64 POP_TOP
  66 JUMP_BACKWARD           18 (to 32)
  68 LOAD_CONST               0 (None)
  70 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f6,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               1 (0)
   4 STORE_FAST               0 (a)
   6 LOAD_GLOBAL              1 (NULL + range)
  18 LOAD_CONST               2 (10)
  20 PRECALL                  1
  24 CALL                     1
  34 GET_ITER
  36 FOR_ITER                 7 (to 52)
  38 STORE_FAST               1 (i)
  40 LOAD_FAST                0 (a)
  42 LOAD_CONST               3 (1)
  44 BINARY_OP               13 (+=)
  48 STORE_FAST               0 (a)
  50 JUMP_BACKWARD            8 (to 36)
  52 LOAD_GLOBAL              3 (NULL + print)
  64 LOAD_FAST                0 (a)
  66 PRECALL                  1
  70 CALL                     1
  80 POP_TOP
  82 LOAD_CONST               0 (None)
  84 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f8,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               1 ((1, 2))
   4 UNPACK_SEQUENCE          2
   8 STORE_FAST               0 (x)
  10 STORE_FAST               1 (y)
  12 LOAD_CONST               0 (None)
  14 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f9,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               1 (1)
   4 LOAD_CONST               1 (1)
   6 COMPARE_OP               2 (==)
  12 POP_JUMP_FORWARD_IF_FALSE     2 (to 18)
  14 LOAD_CONST               1 (1)
  16 JUMP_FORWARD             1 (to 20)
  18 LOAD_CONST               2 (2)
  20 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f10,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_GLOBAL              1 (NULL + range)
  14 LOAD_CONST               1 (10)
  16 PRECALL                  1
  20 CALL                     1
  30 GET_ITER
  32 FOR_ITER                11 (to 56)
  34 STORE_FAST               0 (i)
  36 LOAD_FAST                0 (i)
  38 LOAD_CONST               2 (3)
  40 COMPARE_OP               2 (==)
  46 POP_JUMP_FORWARD_IF_FALSE     3 (to 54)
  48 POP_TOP
  50 LOAD_CONST               0 (None)
  52 RETURN_VALUE
  54 JUMP_BACKWARD           12 (to 32)
  56 LOAD_CONST               0 (None)
  58 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f11,
        expected_dis_out='''\
   0 RESUME                   0
   2 BUILD_LIST               0
   4 LOAD_CONST               1 ((1, 2, 3))
   6 LIST_EXTEND              1
   8 STORE_FAST               0 (list_)
  10 LOAD_CONST               2 (1)
  12 LOAD_CONST               3 (2)
  14 LOAD_CONST               4 (('a', 'b'))
  16 BUILD_CONST_KEY_MAP      2
  18 STORE_FAST               1 (dict_)
  20 LOAD_FAST                0 (list_)
  22 LOAD_FAST                1 (dict_)
  24 BUILD_TUPLE              2
  26 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f12,
        expected_dis_out='''\
   0 RESUME                   0
   2 LOAD_CONST               1 (1)
   4 STORE_FAST               0 (a)
   6 LOAD_CONST               2 (2)
   8 STORE_FAST               1 (b)
  10 LOAD_CONST               3 (3)
  12 STORE_FAST               2 (c)
  14 LOAD_CONST               4 (4)
  16 STORE_FAST               3 (d)
  18 LOAD_CONST               5 (5)
  20 STORE_FAST               4 (e)
  22 LOAD_FAST                0 (a)
  24 LOAD_FAST                1 (b)
  26 LOAD_FAST                2 (c)
  28 BINARY_OP                5 (*)
  32 LOAD_FAST                3 (d)
  34 LOAD_FAST                4 (e)
  36 BINARY_OP                8 (**)
  40 BINARY_OP               11 (/)
  44 BINARY_OP                0 (+)
  48 RETURN_VALUE
'''
    ),
]


def test_version() -> None:
    """
    To do this task you need python=3.11.5
    """
    assert '3.11.5' == sys.version.split(' ', maxsplit=1)[0]


def strip_dis_out(dis_out: str) -> str:
    """Strip first 11 chars from dis_out and remove empty lines"""
    return '\n'.join(line[11:] for line in dis_out.split('\n') if line) + '\n'


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_byteme(t: Case) -> None:
    out = io.StringIO()
    dis.dis(t.func, file=out)
    actual_dis_out = out.getvalue()
    print(actual_dis_out)
    assert strip_dis_out(actual_dis_out) == t.expected_dis_out
