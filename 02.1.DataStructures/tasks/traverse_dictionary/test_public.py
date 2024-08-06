import copy
import dataclasses
import typing as tp

import pytest
import testlib

from .traverse_dictionary import traverse_dictionary_immutable, traverse_dictionary_mutable, \
    traverse_dictionary_iterative


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(traverse_dictionary_immutable)
    assert testlib.is_function_docstring_exists(traverse_dictionary_mutable)
    assert testlib.is_function_docstring_exists(traverse_dictionary_iterative)


###################
# Tests
###################


@dataclasses.dataclass
class Case:
    dct: tp.Mapping[str, tp.Any]
    result: tp.Sequence[tuple[str, int]]

    def __str__(self) -> str:
        return 'parse_{}'.format(self.dct)


TEST_CASES = [
    Case(dct={}, result=[]),
    Case(dct={"a": 1}, result=[("a", 1)]),
    Case(dct={"a": 1, "b": 2}, result=[("a", 1), ("b", 2)]),
    Case(dct={"a": 1, "b": 2, "c": {"d": 3}}, result=[("a", 1), ("b", 2), ("c.d", 3)]),
    Case(dct={"a": 1, "b": 2, "c": {"d": 3, "e": 4}}, result=[("a", 1), ("b", 2), ("c.d", 3), ("c.e", 4)]),
    Case(dct={"a": 1, "b": 2, "c": {"d": 3, "e": 4}, "f": 5},
         result=[("a", 1), ("b", 2), ("c.d", 3), ("c.e", 4), ("f", 5)]),
    Case(dct={"a": 1, "b": 2, "c": {"d": 3, "e": {"g": 7}}, "f": 5},
         result=[("a", 1), ("b", 2), ("c.d", 3), ("f", 5), ("c.e.g", 7)]),
    Case(dct={"a": 1, "b": 2, "c": {"d": 3, "e": {"g": 7}}, "f": 5, "h": {"r": 1}},
         result=[("a", 1), ("b", 2), ("c.d", 3), ("f", 5), ("c.e.g", 7), ("h.r", 1)]),
    Case(dct={"a": 1, "b": 2, "c": {"d": 3, "e": {"g": 7}, "m": 1}, "f": 5, "h": {"r": 1}},
         result=[("a", 1), ("b", 2), ("c.d", 3), ("f", 5), ("c.e.g", 7), ("h.r", 1), ("c.m", 1)]),
    Case(dct={"a": {"b": {"c": {"d": {"e": 1}}}}},
         result=[("a.b.c.d.e", 1)]),
]


def make_very_very_deep_case(n: int) -> Case:
    dct: dict[str, tp.Any] = {}

    dct_inner = dct
    result_key = []
    for i in range(n):
        key = str(i)
        dct_inner[key] = {}
        dct_inner = dct_inner[key]
        result_key.append(key)

    key = str(n + 1)
    dct_inner[key] = 1
    result_key.append(key)

    return Case(dct=dct, result=[(".".join(result_key), 1)])


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_traverse_dictionary_immutable(t: Case) -> None:
    given_dct = copy.deepcopy(t.dct)

    answer = traverse_dictionary_immutable(given_dct)

    assert t.dct == given_dct, "You shouldn't change input dict"

    assert sorted(answer) == sorted(t.result)


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_traverse_dictionary_mutable(t: Case) -> None:
    given_dct = copy.deepcopy(t.dct)

    result: list[tuple[str, int]] = []
    traverse_dictionary_mutable(given_dct, result)

    assert t.dct == given_dct, "You shouldn't change input dict"

    assert sorted(result) == sorted(t.result)


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_traverse_dictionary_iterative(t: Case) -> None:
    given_dct = copy.deepcopy(t.dct)

    result = traverse_dictionary_iterative(given_dct)

    assert t.dct == given_dct, "You shouldn't change input dict"
    assert sorted(result) == sorted(t.result)


def test_traverse_dictionary_iterative_deep_dict() -> None:
    t = make_very_very_deep_case(100000)

    result = traverse_dictionary_iterative(t.dct)

    assert sorted(result) == sorted(t.result)
