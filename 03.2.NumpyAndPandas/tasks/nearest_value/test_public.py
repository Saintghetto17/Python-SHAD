import dataclasses

import numpy as np
import numpy.typing as npt
import pytest

from .nearest_value import nearest_value


@dataclasses.dataclass
class NearestValueCase:
    matrix: npt.NDArray[np.float_]
    value: float
    result: float | None


NEAREST_VALUE_TEST_CASES = [
    NearestValueCase(
        matrix=np.arange(0, 10).reshape((2, 5)).astype(np.float_),
        value=3.6,
        result=4.
    ),
    NearestValueCase(
        matrix=np.arange(0, 10).reshape((5, 2)).astype(np.float_),
        value=0.3,
        result=0.0
    ),
    NearestValueCase(
        matrix=np.arange(0, 10).reshape((10, 1)).astype(np.float_),
        value=0.6,
        result=1.0
    ),
    NearestValueCase(
        matrix=np.zeros((5, 10)),
        value=20.0,
        result=0.0
    ),
    NearestValueCase(
        matrix=np.array([[1, 0, 0]]),
        value=0.9,
        result=1.0
    ),
    NearestValueCase(
        matrix=np.array([[0, 0, 1]]),
        value=0.9,
        result=1.0
    ),
    NearestValueCase(
        matrix=np.array([[1]]),
        value=1000000,
        result=1.0
    ),
    NearestValueCase(
        matrix=np.array([[]]),
        value=0,
        result=None
    ),
]


@pytest.mark.parametrize('t', NEAREST_VALUE_TEST_CASES, ids=str)
def test_construct_matrix(t: NearestValueCase) -> None:
    _val = nearest_value(t.matrix, t.value)
    if _val is None:
        assert t.result is None
    else:
        assert t.result is not None
        assert np.isclose(_val, t.result)


def test_random_matrix() -> None:
    np.random.seed(42)
    for _ in range(100):
        shape = np.random.randint(2, 100, size=2)
        matrix = np.random.rand(*shape)
        for value in np.random.choice(np.ravel(matrix), 10):
            _val = nearest_value(matrix, value)
            if _val is None:
                assert value is None
            else:
                assert np.isclose(_val, value)
