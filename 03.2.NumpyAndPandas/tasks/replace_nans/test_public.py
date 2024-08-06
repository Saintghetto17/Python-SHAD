import dataclasses

import numpy as np
import numpy.typing as npt
import pytest
from numpy.testing import assert_array_equal

from .replace_nans import replace_nans


@dataclasses.dataclass
class ReplaceNansCase:
    matrix: npt.NDArray[np.float_]
    result: npt.NDArray[np.float_]


REPLACE_NANS_TEST_CASES = [
    ReplaceNansCase(
        matrix=np.array([[np.nan,  1,  2,  3], [4, np.nan,  5, np.nan]]),
        result=np.array([[3, 1, 2, 3], [4, 3, 5, 3]])),
    ReplaceNansCase(
        matrix=np.ones((3, 14)) * np.nan,
        result=np.zeros((3, 14))),
    ReplaceNansCase(
        matrix=np.array([[]]),
        result=np.array([[]])),
    ReplaceNansCase(
        matrix=np.array([[3]]),
        result=np.array([[3]])),
    ReplaceNansCase(
        matrix=np.array([[np.nan]]),
        result=np.array([[0]])),
    ReplaceNansCase(
        matrix=np.array([[1, np.nan]]),
        result=np.array([[1, 1]])),
    ReplaceNansCase(
        matrix=np.array([[0, np.nan,  2,  3,  4.],
                         [5,  6,  7,  8, np.nan],
                         [np.nan, 11, 12, 13, 14.],
                         [15, 16, 17, np.nan, 19.],
                         [20, 21, np.nan, 23, 24.]]),
        result=np.array([[0, 12,  2,  3,  4.],
                         [5,  6,  7,  8, 12.],
                         [12, 11, 12, 13, 14.],
                         [15, 16, 17, 12, 19.],
                         [20, 21, 12, 23, 24.]]))

]


@pytest.mark.parametrize('t', REPLACE_NANS_TEST_CASES, ids=str)
def test_construct_matrix(t: ReplaceNansCase) -> None:
    assert_array_equal(replace_nans(t.matrix), t.result)
