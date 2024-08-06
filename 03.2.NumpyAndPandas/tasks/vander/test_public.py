import dataclasses

import numpy as np
import numpy.typing as npt
import pytest
from numpy.testing import assert_array_equal

from .vander import vander


@dataclasses.dataclass
class VanderCase:
    array: npt.NDArray[np.float_ | np.int_]
    result: npt.NDArray[np.float_]


VANDER_TEST_CASES = [
    VanderCase(
        array=np.array([1]),
        result=np.array([[1]])),
    VanderCase(
        array=np.array([1, 2, 3]),
        result=np.array([[1, 1, 1], [1, 2, 4], [1, 3, 9]])),
    VanderCase(
        array=np.ones(3),
        result=np.ones((3, 3)))
]


@pytest.mark.parametrize('t', VANDER_TEST_CASES, ids=str)
def test_construct_matrix(t: VanderCase) -> None:
    assert_array_equal(vander(t.array), t.result)


def test_random_matrix() -> None:
    np.random.seed(42)

    for _ in range(100):
        matrix = np.random.randint(1, 10, 10)
        assert_array_equal(vander(matrix), np.vander(matrix, increasing=True))
