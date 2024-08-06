import copy
import dataclasses
import itertools

import pytest
import testlib

from .bin_tricky import find_median


@dataclasses.dataclass
class Case:
    nums1: list[int]
    nums2: list[int]

    def __str__(self) -> str:
        return 'find_median_in_{}_and_{}'.format(self.nums1, self.nums2)


BIG_VALUE = 10**5


def get_range_with_peak_on_position(range_size: int, position: int) -> list[int]:
    if position >= range_size or position < 0:
        raise ValueError("Position should be in [0, range_size)")

    return list(itertools.chain(range(position), [range_size + 1], range(range_size - position - 1, position, -1)))


TEST_CASES = [
    Case(nums1=[1], nums2=[2]),
    Case(nums1=[], nums2=[2]),
    Case(nums1=[1], nums2=[]),
    Case(nums1=[1, 2], nums2=[]),
    Case(nums1=[1, 2, 3], nums2=[]),
    Case(nums1=[1, 2, 3, 5], nums2=[]),
    Case(nums1=[1, 2, 3, 5, 7], nums2=[]),
    Case(nums1=[-1, -1, -1], nums2=[-1, -1, -1]),
    Case(nums1=[1, 2],  nums2=[1, 2]),
    Case(nums1=[1, 1], nums2=[1, 1]),
    Case(nums1=[1, 3], nums2=[2]),
    Case(nums1=[2], nums2=[1, 3, 4]),
    Case(nums1=[3], nums2=[1, 2, 4]),
    Case(nums1=[2, 6], nums2=[3, 4]),
    Case(nums1=[1, 2, 2, 2, 3, 4, 5], nums2=[1, 2, 6, 7, 8, 8, 9]),
    Case(nums1=[1, 2, 2, 2, 3, 4, 5], nums2=[1, 2, 6]),
    Case(nums1=[1, 2, 2, 2, 2, 2, 5], nums2=[1, 2, 6]),
    Case(nums1=[1, 2, 3, 4, 5], nums2=[1, 2, 3]),
    Case(nums1=[2, 2, 2, 2, 2, 2, 2, 2], nums2=[2, 2, 2]),
    Case(nums1=[2, 2, 2, 2, 2, 2, 2, 2], nums2=[2, 2, 2, 2]),
    Case(nums1=[1, 2, 3, 4], nums2=[3, 4, 5, 6]),
    Case(nums1=[1, 2, 3, 4], nums2=[1, 2, 3, 4]),
    Case(nums1=[1, 3, 5, 7], nums2=[2, 4, 6, 8]),
    Case(nums1=[1, 3, 5, 7], nums2=[-1, 2, 4, 6, 8]),
    Case(nums1=[1, 3, 5, 7], nums2=[-1, -1, -1]),
    Case(nums1=[-1, 5, 8, 17], nums2=[-7, 15, 20]),
    Case(nums1=[-1, 5, 8, 17], nums2=[21, 25, 38]),
    Case(nums1=[1, 3, 5, 7], nums2=[-5, -4, 0]),
    Case(nums1=[1, 2], nums2=[3]),
    Case(nums1=[1], nums2=[2, 3]),
    Case(nums1=[1, 2], nums2=[3, 4]),
    Case(nums1=[3, 4, 5], nums2=[1]),
    Case(nums1=[3, 4, 5, 6, 7, 8], nums2=[1, 2]),
    Case(nums1=[1, 1, 2, 5, 6], nums2=[1, 9, 10]),
    Case(nums1=list(range(0, 100, 2)), nums2=list(range(-100, 100, 5))),
]


###################
# Structure asserts
###################


def test_find_median_structure() -> None:
    assert not testlib.is_global_used(find_median, 'sorted'), \
        "You should use iteration ONLY, not manually sorting"
    assert not testlib.is_bytecode_op_used(find_median, 'CONTAINS_OP'), \
        "You, don't even dare to use `in`! It's plainly illegal, you got that?!"


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(find_median)


###################
# Tests
###################


def dummy_implementation(nums1: list[int], nums2: list[int]) -> float:
    combined_nums = sorted(nums1 + nums2)
    m = len(nums1)
    n = len(nums2)
    return (combined_nums[(m + n) // 2] + combined_nums[(m + n - 1) // 2]) / 2


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_find_value(t: Case) -> None:
    nums1_copy, nums2_copy = copy.deepcopy(t.nums1), copy.deepcopy(t.nums2)

    answer = find_median(nums1_copy, nums2_copy)

    assert isinstance(answer, float), "You shouldn't return different types from the same function"

    assert nums1_copy == t.nums1 and nums2_copy == t.nums2, "You shouldn't change input"

    ground_truth = dummy_implementation(t.nums1, t.nums2)

    assert answer == ground_truth

    swapped_args_answer = find_median(t.nums1, t.nums2)
    assert swapped_args_answer == ground_truth, "You should get the same result if you swap the arguments"
