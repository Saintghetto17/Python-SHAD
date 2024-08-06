from types import FunctionType
import dataclasses

import pytest

from .life_game import LifeGame


@dataclasses.dataclass
class Case:
    board: list[list[int]]
    expected: list[list[int]]
    generation_number: int


TESTS = [
    Case(
        board=[
            [0, 2, 0],
            [0, 2, 0],
            [0, 2, 0]
        ],
        expected=[
            [0, 0, 0],
            [2, 2, 2],
            [0, 0, 0]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [0, 0, 0, 0],
            [0, 3, 3, 0],
            [0, 3, 3, 0],
            [0, 1, 0, 1]
        ],
        expected=[
            [0, 0, 0, 0],
            [0, 3, 3, 0],
            [0, 3, 3, 0],
            [0, 1, 0, 1]
        ],
        generation_number=7
    ),
    Case(
        board=[
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]
        ],
        expected=[
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]
        ],
        generation_number=2
    ),
    Case(
        board=[
            [0, 0, 0, 0],
            [0, 3, 0, 0],
            [0, 3, 0, 0],
            [0, 0, 3, 0],
            [0, 0, 0, 0]
        ],
        expected=[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 3, 3, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        expected=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 2, 0],
            [0, 2, 0, 0, 0, 0, 0, 2, 0],
            [0, 2, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        generation_number=9
    ),
    Case(
        board=[
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 3, 0, 3, 1, 0, 0],
            [0, 1, 0, 0, 3, 1, 3, 0, 0, 1],
            [0, 0, 0, 1, 3, 0, 3, 1, 0, 0],
            [0, 1, 0, 0, 3, 1, 3, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        ],
        expected=[
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 3, 3, 1, 3, 3, 0, 1],
            [0, 0, 0, 1, 3, 0, 3, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        ],
        generation_number=9
    ),
    Case(
        board=[
            [0, 1, 2, 3, 0],
            [2, 3, 0, 1, 2],
            [0, 1, 2, 3, 0],
            [2, 3, 0, 1, 2],
            [0, 1, 2, 3, 0]
        ],
        expected=[
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0]
        ],
        generation_number=2
    ),
    Case(
        board=[
            [3, 3, 3, 3, 3],
            [0, 0, 0, 0, 0],
            [3, 3, 3, 3, 3],
            [0, 0, 0, 0, 0],
            [3, 3, 3, 3, 3]
        ],
        expected=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        generation_number=10
    ),
    Case(
        board=[
            [0]
        ],
        expected=[
            [0]
        ],
        generation_number=100000
    ),
    Case(
        board=[
            [1]
        ],
        expected=[
            [1]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [2]
        ],
        expected=[
            [0]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [3]
        ],
        expected=[
            [0]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [2],
            [2]
        ],
        expected=[
            [0],
            [0]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [3],
            [3]
        ],
        expected=[
            [0],
            [0]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [2, 2],
            [2, 2]
        ],
        expected=[
            [2, 2],
            [2, 2]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [3, 3],
            [3, 3]
        ],
        expected=[
            [3, 3],
            [3, 3]
        ],
        generation_number=1
    ),
    Case(
        board=[
            [3, 3, 0],
            [3, 0, 2],
            [0, 2, 2]
        ],
        expected=[
            [3, 3, 0],
            [3, 2, 2],
            [0, 2, 2]
        ],
        generation_number=1
    ),
]


###################
# Structure asserts
###################

def test_methods() -> None:
    methods_names = [x for x, y in LifeGame.__dict__.items() if isinstance(y, FunctionType)]
    private_methods = {x for x in methods_names if x.startswith('_')}
    public_methods = {x for x in methods_names if not x.startswith('_')}
    assert public_methods == {'get_next_generation'}
    assert len(private_methods - {'__init__'}) > 0


###################
# Tests
###################

@pytest.mark.parametrize("test_case", TESTS)
def test_life_game(test_case: Case) -> None:
    game = LifeGame(test_case.board)
    generation = None
    for _ in range(test_case.generation_number):
        generation = game.get_next_generation()
    assert generation == test_case.expected
