import copy
import dataclasses
import itertools
import typing as tp

import pytest
import testlib
import heapq

from .merge_lists import merge


###################
# Structure asserts
###################


def test_banned_modules() -> None:
    assert testlib.is_module_imported_hard('heapq'), 'You should use heapq'


def test_merge_structure() -> None:
    assert not testlib.is_global_used(merge, 'sorted'), 'You should use iteration ONLY, not manually sorting'
    assert not testlib.is_bytecode_op_used(merge, 'BUILD_SLICE'), 'You should use iteration ONLY, not slicing'


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(merge)


###################
# Tests
###################


@dataclasses.dataclass
class Case:
    lists: tp.Sequence[tp.Sequence[int]]
    name: str

    def __str__(self) -> str:
        return 'merge_{}'.format(self.name)


def make_test_cases() -> tp.Generator[Case, None, None]:
    for i in range(10):
        lists: list[list[int]] = [[] for i in range(i + 1)]

        for j in range(2000):
            basket = j % (i + 1)
            lists[basket].append(j)
        yield Case(lists=lists, name='list_' + str(i))

    yield Case(lists=[], name='list_empty')
    yield Case(lists=[[], [], []], name='list_with_empty_lists')

    for i in range(10):
        lists = [[] for i in range(i + 1)]
        for j in range(2000):
            basket = j // (2000 // (i + 1) + 1)
            lists[basket].append(j)

        yield Case(lists=lists, name='list_by_blocks_' + str(i))

    for i in range(10):
        lists = [[] for i in range(i + 1)]
        for j in range(2000):
            basket = j // (2000 // (i + 1) + 1)
            lists[basket - (basket % 2)].append(j)

        yield Case(lists=lists, name='list_by_blocks_with_gaps' + str(i))

    yield Case(lists=[[1], [1]], name='lists_with_same_elements')


@pytest.mark.parametrize('t', list(make_test_cases()), ids=str)
def test_merge(t: Case, mocker: tp.Any) -> None:
    _ = mocker.patch("heapq.merge")

    given_lists = copy.deepcopy(t.lists)

    answer = merge(given_lists)

    if heapq.merge.call_count > 0:  # type: ignore
        assert False, "heapq.merge is banned"

    assert answer == sorted(itertools.chain(*t.lists))

    assert t.lists == given_lists, "You shouldn't change inputs"
