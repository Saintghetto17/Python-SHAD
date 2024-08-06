import dataclasses
from os.path import normpath
import timeit
from pathlib import Path

import pytest
import testlib

from .normalize_path import normalize_path


@dataclasses.dataclass
class Case:
    path: str
    result: str


TEST_CASES = [
    Case(path='foo', result='foo'),
    Case(path='./bar', result='bar'),
    Case(path='', result='.'),
    Case(path='.', result='.'),
    Case(path='/', result='/'),
    Case(path='//', result='/'),
    Case(path='/..//..//././///././/..//../', result='/'),
    Case(path='..', result='..'),
    Case(path='../', result='..'),
    Case(path='../..', result='../..'),
    Case(path='a/b/c/d/../../../..', result='.'),
    Case(path='zog/..', result='.'),
    Case(path='./config/../etc', result='etc'),
    Case(path='foo/./bar', result='foo/bar'),
    Case(path='a/..///../b', result='../b'),
    Case(path='./../../../zog', result='../../../zog'),
    Case(path='/////documents/root/.././../etc', result='/etc'),
    Case(path='/../../../zog', result='/zog'),
    Case(path='/foo/bar//baz/asdf/quux/..', result='/foo/bar/baz/asdf'),
    Case(path='/h/../a/..' * 1_000, result='/'),
    Case(path='/a/b//c/d/..//../..//..' * 1_000, result='/'),
    Case(path='a/b//c/d/..//../..//../' * 1_000, result='.'),
]


@dataclasses.dataclass
class LoadCase:
    path: str
    num: int


LOAD_TEST_CASES = [
    LoadCase(path='/h/..' * 1_000_000, num=1),
    # LoadCase(path='/h/../a/..' * 1_000_000, num=1),
    # LoadCase(path='/a/b//..//../' * 1_000_000, num=1),
    LoadCase(path='/a/b//c/d/..//../..//..' * 1_000_000, num=1),
]


###################
# Structure asserts
###################


def test_banned_modules() -> None:
    assert not testlib.is_module_imported(
        'pathlib', Path(__file__).parent / 'normalize_path.py'
    ), 'You should not use `pathlib` module'
    assert not testlib.is_instruction_used(normalize_path, 'argval', 'normpath')


###################
# Tests
###################


@pytest.mark.parametrize('case', TEST_CASES)
def test_normalize(case: Case) -> None:
    answer = normalize_path(case.path)

    assert answer == case.result


@pytest.mark.parametrize('case', LOAD_TEST_CASES)
def test_speed(case: LoadCase) -> None:
    solution_time = timeit.timeit(lambda: normalize_path(case.path), number=case.num) / case.num
    normpath_time = timeit.timeit(lambda: normpath(case.path), number=case.num) / case.num

    # in python 3.11 it was speed up a lot, so.. you need to be at list 25 times slower for now
    assert solution_time < normpath_time * 25, 'You should do this in a more optimal way'
