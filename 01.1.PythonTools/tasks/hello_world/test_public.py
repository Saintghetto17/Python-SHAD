import pytest

from .hello_world import get_hello_world


class Case:
    def __init__(self, name: str, expected: str):
        self._name = name
        self.expected = expected

    def __str__(self) -> str:
        return 'test_{}'.format(self._name)


TEST_CASES = [
    Case(name='basic', expected='Hello world!')
]


@pytest.mark.parametrize('test_case', TEST_CASES, ids=str)
def test_hello_world(test_case: Case) -> None:
    answer = get_hello_world()
    assert answer == test_case.expected
