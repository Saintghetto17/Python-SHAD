import dataclasses

import numpy as np
import numpy.typing as npt
import pytest

from .max_element import max_element


@dataclasses.dataclass
class MaxElementCase:
    array: npt.NDArray[np.int_]
    result: int | None


MAX_ELEMENT_TEST_CASES = [
    MaxElementCase(
        array=np.array([1, 0, 2, 3]),
        result=2
    ),
    MaxElementCase(
        array=np.array([6, 2, 0, 3, 0, 0, 5, 7, 0]),
        result=5
    ),
    MaxElementCase(
        array=np.array([6, 6]),
        result=None
    ),
    MaxElementCase(
        array=np.zeros(3, dtype=np.int_),
        result=0
    ),
    MaxElementCase(
        array=np.array([0, 1]),
        result=1
    ),
    MaxElementCase(
        array=np.array([1, 0]),
        result=None
    ),
    MaxElementCase(
        array=np.array([1, 0, 0, -1]),
        result=0
    ),
    MaxElementCase(
        array=np.array([0]),
        result=None
    ),
    MaxElementCase(
        array=np.array([1]),
        result=None
    ),
    MaxElementCase(
        array=np.array([0, 1, 2, 0, 10]),
        result=10
    ),
    MaxElementCase(
        array=np.array([6, 2, 0, 3, 0, 0, 9, 4]),
        result=9
    ),
]


@pytest.mark.parametrize('t', MAX_ELEMENT_TEST_CASES, ids=str)
def test_construct_matrix(t: MaxElementCase) -> None:
    assert max_element(t.array) == t.result
