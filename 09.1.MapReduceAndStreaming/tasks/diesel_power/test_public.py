import copy
import dataclasses
import time
import typing as tp

import pytest
from pytest import approx

from . import operations as ops
from . import memory_watchdog

KiB = 1024
MiB = 1024 * KiB


class _Key:
    def __init__(self, *args: str) -> None:
        self._items = sorted(args)

    def __call__(self, d: tp.Mapping[str, tp.Any]) -> tuple[str, ...]:
        return tuple(str(d.get(key)) for key in self._items)


@dataclasses.dataclass
class MapCase:
    mapper: ops.Mapper
    data: list[ops.TRow]
    ground_truth: list[ops.TRow]
    cmp_keys: tuple[str, ...]
    mapper_item: int = 0
    mapper_ground_truth_items: tuple[int, ...] = (0,)


MAP_CASES = [
    MapCase(
        mapper=ops.DummyMapper(),
        data=[
            {'test_id': 1, 'text': 'one two three'},
            {'test_id': 2, 'text': 'testing out stuff'}
        ],
        ground_truth=[
            {'test_id': 1, 'text': 'one two three'},
            {'test_id': 2, 'text': 'testing out stuff'}
        ],
        cmp_keys=('test_id', 'text')
    ),
    MapCase(
        mapper=ops.LowerCase(column='text'),
        data=[
            {'test_id': 1, 'text': 'camelCaseTest'},
            {'test_id': 2, 'text': 'UPPER_CASE_TEST'},
            {'test_id': 3, 'text': 'wEiRdTeSt'}
        ],
        ground_truth=[
            {'test_id': 1, 'text': 'camelcasetest'},
            {'test_id': 2, 'text': 'upper_case_test'},
            {'test_id': 3, 'text': 'weirdtest'}
        ],
        cmp_keys=('test_id', 'text')
    ),
    MapCase(
        mapper=ops.FilterPunctuation(column='text'),
        data=[
            {'test_id': 1, 'text': 'Hello, world!'},
            {'test_id': 2, 'text': 'Test. with. a. lot. of. dots.'},
            {'test_id': 3, 'text': r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'}
        ],
        ground_truth=[
            {'test_id': 1, 'text': 'Hello world'},
            {'test_id': 2, 'text': 'Test with a lot of dots'},
            {'test_id': 3, 'text': ''}
        ],
        cmp_keys=('test_id', 'text')
    ),
    MapCase(
        mapper=ops.Split(column='text'),
        data=[
            {'test_id': 1, 'text': 'one two three'},
            {'test_id': 2, 'text': 'tab\tsplitting\ttest'},
            {'test_id': 3, 'text': 'more\nlines\ntest'},
            {'test_id': 4, 'text': 'tricky\u00A0test'}
        ],
        ground_truth=[
            {'test_id': 1, 'text': 'one'},
            {'test_id': 1, 'text': 'three'},
            {'test_id': 1, 'text': 'two'},

            {'test_id': 2, 'text': 'splitting'},
            {'test_id': 2, 'text': 'tab'},
            {'test_id': 2, 'text': 'test'},

            {'test_id': 3, 'text': 'lines'},
            {'test_id': 3, 'text': 'more'},
            {'test_id': 3, 'text': 'test'},

            {'test_id': 4, 'text': 'test'},
            {'test_id': 4, 'text': 'tricky'}
        ],
        cmp_keys=('test_id', 'text'),
        mapper_ground_truth_items=(0, 1, 2)
    ),
    MapCase(
        mapper=ops.Split(column='text', separator=';'),
        data=[
            {'test_id': 1, 'text': 'one;two;three'},
            {'test_id': 2, 'text': 'tab;splitting;test'},
            {'test_id': 3, 'text': 'more;lines;test'},
            {'test_id': 4, 'text': 'tricky;test'}
        ],
        ground_truth=[
            {'test_id': 1, 'text': 'one'},
            {'test_id': 1, 'text': 'three'},
            {'test_id': 1, 'text': 'two'},

            {'test_id': 2, 'text': 'splitting'},
            {'test_id': 2, 'text': 'tab'},
            {'test_id': 2, 'text': 'test'},

            {'test_id': 3, 'text': 'lines'},
            {'test_id': 3, 'text': 'more'},
            {'test_id': 3, 'text': 'test'},

            {'test_id': 4, 'text': 'test'},
            {'test_id': 4, 'text': 'tricky'}
        ],
        cmp_keys=('test_id', 'text'),
        mapper_ground_truth_items=(0, 1, 2)
    ),
    MapCase(
        mapper=ops.Product(columns=['speed', 'distance'], result_column='time'),
        data=[
            {'test_id': 1, 'speed': 5, 'distance': 10},
            {'test_id': 2, 'speed': 60, 'distance': 2},
            {'test_id': 3, 'speed': 3, 'distance': 15},
            {'test_id': 4, 'speed': 100, 'distance': 0.5},
            {'test_id': 5, 'speed': 48, 'distance': 15},
        ],
        ground_truth=[
            {'test_id': 1, 'speed': 5, 'distance': 10, 'time': 50},
            {'test_id': 2, 'speed': 60, 'distance': 2, 'time': 120},
            {'test_id': 3, 'speed': 3, 'distance': 15, 'time': 45},
            {'test_id': 4, 'speed': 100, 'distance': 0.5, 'time': 50},
            {'test_id': 5, 'speed': 48, 'distance': 15, 'time': 720},
        ],
        cmp_keys=('test_id', 'speed', 'distance', 'time')
    ),
    MapCase(
        mapper=ops.Filter(condition=lambda row: row['f'] ^ row['g']),
        data=[
            {'test_id': 1, 'f': 0, 'g': 0},
            {'test_id': 2, 'f': 0, 'g': 1},
            {'test_id': 3, 'f': 1, 'g': 0},
            {'test_id': 4, 'f': 1, 'g': 1}
        ],
        ground_truth=[
            {'test_id': 2, 'f': 0, 'g': 1},
            {'test_id': 3, 'f': 1, 'g': 0}
        ],
        cmp_keys=('test_id', 'f', 'g'),
        mapper_ground_truth_items=tuple()
    ),
    MapCase(
        mapper=ops.Project(columns=['value']),
        data=[
            {'test_id': 1, 'junk': 'x', 'value': 42},
            {'test_id': 2, 'junk': 'y', 'value': 1},
            {'test_id': 3, 'junk': 'z', 'value': 144}
        ],
        ground_truth=[
            {'value': 42},
            {'value': 1},
            {'value': 144}
        ],
        cmp_keys=('value',)
    )
]


@pytest.mark.parametrize('case', MAP_CASES)
def test_mapper(case: MapCase) -> None:
    mapper_data_row = copy.deepcopy(case.data[case.mapper_item])
    mapper_ground_truth_rows = [copy.deepcopy(case.ground_truth[i]) for i in case.mapper_ground_truth_items]

    key_func = _Key(*case.cmp_keys)

    mapper_result = case.mapper(mapper_data_row)
    assert isinstance(mapper_result, tp.Iterator)
    assert sorted(mapper_result, key=key_func) == sorted(mapper_ground_truth_rows, key=key_func)

    result = ops.Map(case.mapper)(iter(case.data))
    assert isinstance(result, tp.Iterator)
    assert sorted(result, key=key_func) == sorted(case.ground_truth, key=key_func)


@dataclasses.dataclass
class ReduceCase:
    reducer: ops.Reducer
    reducer_keys: tuple[str, ...]
    data: list[ops.TRow]
    ground_truth: list[ops.TRow]
    cmp_keys: tuple[str, ...]
    reduce_data_items: tuple[int, ...] = (0,)
    reduce_ground_truth_items: tuple[int, ...] = (0,)


REDUCE_CASES = [
    ReduceCase(
        reducer=ops.FirstReducer(),
        reducer_keys=('test_id',),
        data=[
            {'test_id': 1, 'text': 'hello, world'},
            {'test_id': 2, 'text': 'bye!'}
        ],
        ground_truth=[
            {'test_id': 1, 'text': 'hello, world'},
            {'test_id': 2, 'text': 'bye!'}
        ],
        cmp_keys=('test_id', 'text')
    ),
    ReduceCase(
        reducer=ops.TopN(column='rank', n=3),
        reducer_keys=('match_id',),
        data=[
            {'match_id': 1, 'player_id': 1, 'rank': 42},
            {'match_id': 1, 'player_id': 2, 'rank': 7},
            {'match_id': 1, 'player_id': 3, 'rank': 0},
            {'match_id': 1, 'player_id': 4, 'rank': 39},

            {'match_id': 2, 'player_id': 5, 'rank': 15},
            {'match_id': 2, 'player_id': 6, 'rank': 39},
            {'match_id': 2, 'player_id': 7, 'rank': 27},
            {'match_id': 2, 'player_id': 8, 'rank': 7}
        ],
        ground_truth=[
            {'match_id': 1, 'player_id': 1, 'rank': 42},
            {'match_id': 1, 'player_id': 2, 'rank': 7},
            {'match_id': 1, 'player_id': 4, 'rank': 39},

            {'match_id': 2, 'player_id': 5, 'rank': 15},
            {'match_id': 2, 'player_id': 6, 'rank': 39},
            {'match_id': 2, 'player_id': 7, 'rank': 27}
        ],
        cmp_keys=('match_id', 'player_id', 'rank'),
        reduce_data_items=(0, 1, 2, 3),
        reduce_ground_truth_items=(0, 1, 2)
    ),
    ReduceCase(
        reducer=ops.TopN(column='rank', n=2),
        reducer_keys=('match_id',),
        data=[
            {'match_id': 1, 'player_id': 1, 'rank': 5},
            {'match_id': 1, 'player_id': 2, 'rank': 4},
            {'match_id': 1, 'player_id': 3, 'rank': 3},
            {'match_id': 1, 'player_id': 4, 'rank': 2},

            {'match_id': 2, 'player_id': 5, 'rank': 9},
            {'match_id': 2, 'player_id': 6, 'rank': 8},
            {'match_id': 2, 'player_id': 7, 'rank': 7},
            {'match_id': 2, 'player_id': 8, 'rank': 6}
        ],
        ground_truth=[
            {'match_id': 1, 'player_id': 1, 'rank': 5},
            {'match_id': 1, 'player_id': 2, 'rank': 4},

            {'match_id': 2, 'player_id': 5, 'rank': 9},
            {'match_id': 2, 'player_id': 6, 'rank': 8},
        ],
        cmp_keys=("match_id", "player_id", "rank"),
        reduce_data_items=(0, 1, 2, 3),
        reduce_ground_truth_items=(0, 1)
    ),
    ReduceCase(
        reducer=ops.TermFrequency(words_column='text'),
        reducer_keys=('doc_id',),
        data=[
            {'doc_id': 1, 'text': 'hello', 'count': 1},
            {'doc_id': 1, 'text': 'little', 'count': 1},
            {'doc_id': 1, 'text': 'world', 'count': 1},

            {'doc_id': 2, 'text': 'little', 'count': 1},

            {'doc_id': 3, 'text': 'little', 'count': 3},
            {'doc_id': 3, 'text': 'little', 'count': 3},
            {'doc_id': 3, 'text': 'little', 'count': 3},

            {'doc_id': 4, 'text': 'little', 'count': 2},
            {'doc_id': 4, 'text': 'hello', 'count': 1},
            {'doc_id': 4, 'text': 'little', 'count': 2},
            {'doc_id': 4, 'text': 'world', 'count': 1},

            {'doc_id': 5, 'text': 'hello', 'count': 2},
            {'doc_id': 5, 'text': 'hello', 'count': 2},
            {'doc_id': 5, 'text': 'world', 'count': 1},

            {'doc_id': 6, 'text': 'world', 'count': 4},
            {'doc_id': 6, 'text': 'world', 'count': 4},
            {'doc_id': 6, 'text': 'world', 'count': 4},
            {'doc_id': 6, 'text': 'world', 'count': 4},
            {'doc_id': 6, 'text': 'hello', 'count': 1}
        ],
        ground_truth=[
            {'doc_id': 1, 'text': 'hello', 'tf': approx(0.3333, abs=0.001)},
            {'doc_id': 1, 'text': 'little', 'tf': approx(0.3333, abs=0.001)},
            {'doc_id': 1, 'text': 'world', 'tf': approx(0.3333, abs=0.001)},

            {'doc_id': 2, 'text': 'little', 'tf': approx(1.0)},

            {'doc_id': 3, 'text': 'little', 'tf': approx(1.0)},

            {'doc_id': 4, 'text': 'hello', 'tf': approx(0.25)},
            {'doc_id': 4, 'text': 'little', 'tf': approx(0.5)},
            {'doc_id': 4, 'text': 'world', 'tf': approx(0.25)},

            {'doc_id': 5, 'text': 'hello', 'tf': approx(0.666, abs=0.001)},
            {'doc_id': 5, 'text': 'world', 'tf': approx(0.333, abs=0.001)},

            {'doc_id': 6, 'text': 'hello', 'tf': approx(0.2)},
            {'doc_id': 6, 'text': 'world', 'tf': approx(0.8)}
        ],
        cmp_keys=('doc_id', 'text', 'tf'),
        reduce_data_items=(0, 1, 2),
        reduce_ground_truth_items=(0, 1, 2)
    ),
    ReduceCase(
        reducer=ops.Count(column='count'),
        reducer_keys=('word',),
        data=[
            {'sentence_id': 2, 'word': 'hell'},
            {'sentence_id': 1, 'word': 'hello'},
            {'sentence_id': 2, 'word': 'hello'},
            {'sentence_id': 1, 'word': 'little'},
            {'sentence_id': 2, 'word': 'little'},
            {'sentence_id': 2, 'word': 'little'},
            {'sentence_id': 1, 'word': 'my'},
            {'sentence_id': 2, 'word': 'my'},
            {'sentence_id': 1, 'word': 'world'},
        ],
        ground_truth=[
            {'count': 1, 'word': 'hell'},
            {'count': 1, 'word': 'world'},
            {'count': 2, 'word': 'hello'},
            {'count': 2, 'word': 'my'},
            {'count': 3, 'word': 'little'}
        ],
        cmp_keys=('count', 'word'),
        reduce_data_items=(1, 2),
        reduce_ground_truth_items=(2,)
    ),
    ReduceCase(
        reducer=ops.Sum(column='score'),
        reducer_keys=('match_id',),
        data=[
            {'match_id': 1, 'player_id': 1, 'score': 42},
            {'match_id': 1, 'player_id': 2, 'score': 7},
            {'match_id': 1, 'player_id': 3, 'score': 0},
            {'match_id': 1, 'player_id': 4, 'score': 39},

            {'match_id': 2, 'player_id': 5, 'score': 15},
            {'match_id': 2, 'player_id': 6, 'score': 39},
            {'match_id': 2, 'player_id': 7, 'score': 27},
            {'match_id': 2, 'player_id': 8, 'score': 7}
        ],
        ground_truth=[
            {'match_id': 1, 'score': 88},
            {'match_id': 2, 'score': 88}
        ],
        cmp_keys=('test_id', 'text'),
        reduce_data_items=(0, 1, 2, 3),
        reduce_ground_truth_items=(0,)
    )

]


@pytest.mark.parametrize('case', REDUCE_CASES)
def test_reducer(case: ReduceCase) -> None:
    reducer_data_rows = [copy.deepcopy(case.data[i]) for i in case.reduce_data_items]
    reducer_ground_truth_rows = [copy.deepcopy(case.ground_truth[i]) for i in case.reduce_ground_truth_items]

    key_func = _Key(*case.cmp_keys)

    reducer_result = case.reducer(case.reducer_keys, iter(reducer_data_rows))
    assert isinstance(reducer_result, tp.Iterator)
    assert sorted(reducer_result, key=key_func) == sorted(reducer_ground_truth_rows, key=key_func)

    result = ops.Reduce(case.reducer, case.reducer_keys)(iter(case.data))
    assert isinstance(result, tp.Iterator)
    assert sorted(result, key=key_func) == sorted(case.ground_truth, key=key_func)


@dataclasses.dataclass
class JoinCase:
    joiner: ops.Joiner
    join_keys: tp.Sequence[str]
    data_left: list[ops.TRow]
    data_right: list[ops.TRow]
    ground_truth: list[ops.TRow]
    cmp_keys: tuple[str, ...]
    join_data_left_items: tuple[int, ...] = (0,)
    join_data_right_items: tuple[int, ...] = (0,)
    join_ground_truth_items: tuple[int, ...] = (0,)


JOIN_CASES = [
    JoinCase(
        joiner=ops.InnerJoiner(),
        join_keys=('player_id',),
        data_left=[
            {'player_id': 1, 'username': 'XeroX'},
            {'player_id': 2, 'username': 'jay'},
            {'player_id': 3, 'username': 'Destroyer'},
        ],
        data_right=[
            {'game_id': 2, 'player_id': 1, 'score': 17},
            {'game_id': 3, 'player_id': 1, 'score': 22},
            {'game_id': 1, 'player_id': 3, 'score': 99}
        ],
        ground_truth=[
            {'game_id': 1, 'player_id': 3, 'score': 99, 'username': 'Destroyer'},
            {'game_id': 2, 'player_id': 1, 'score': 17, 'username': 'XeroX'},
            {'game_id': 3, 'player_id': 1, 'score': 22, 'username': 'XeroX'}
        ],
        cmp_keys=('game_id', 'player_id', 'score', 'username'),
        join_data_left_items=(0,),
        join_data_right_items=(0, 1),
        join_ground_truth_items=(1, 2)
    ),
    JoinCase(
        joiner=ops.InnerJoiner(),
        join_keys=('player_id',),
        data_left=[
            {'player_id': 0, 'username': 'root'},
            {'player_id': 1, 'username': 'XeroX'},
            {'player_id': 2, 'username': 'jay'}
        ],
        data_right=[
            {'game_id': 2, 'player_id': 1, 'score': 17},
            {'game_id': 3, 'player_id': 2, 'score': 22},
            {'game_id': 1, 'player_id': 3, 'score': 9999999}
        ],
        ground_truth=[
            # player 3 is unknown
            # no games for player 0
            {'game_id': 2, 'player_id': 1, 'score': 17, 'username': 'XeroX'},
            {'game_id': 3, 'player_id': 2, 'score': 22, 'username': 'jay'}
        ],
        cmp_keys=('game_id', 'player_id', 'score', 'username'),
        join_data_left_items=(2,),
        join_data_right_items=(1,),
        join_ground_truth_items=(1,),
    ),
    JoinCase(
        joiner=ops.InnerJoiner(),
        join_keys=('id',),
        data_left=[
            {'id': 1, 'x': 11},
            {'id': 1, 'x': 12},
            {'id': 2, 'x': 21},
            {'id': 2, 'x': 22},
        ],
        data_right=[
            {'id': 1, 'y': 101},
            {'id': 1, 'y': 102},
            {'id': 2, 'y': 201},
            {'id': 2, 'y': 202},
        ],
        ground_truth=[
            {'id': 1, 'x': 11, 'y': 101},
            {'id': 1, 'x': 11, 'y': 102},
            {'id': 1, 'x': 12, 'y': 101},
            {'id': 1, 'x': 12, 'y': 102},
            {'id': 2, 'x': 21, 'y': 201},
            {'id': 2, 'x': 21, 'y': 202},
            {'id': 2, 'x': 22, 'y': 201},
            {'id': 2, 'x': 22, 'y': 202},
        ],
        cmp_keys=('id', 'x', 'y'),
        join_data_left_items=(0, 1),
        join_data_right_items=(0, 1),
        join_ground_truth_items=(0, 1, 2, 3)
    ),
    JoinCase(
        joiner=ops.OuterJoiner(),
        join_keys=('player_id',),
        data_left=[
            {'player_id': 0, 'username': 'root'},
            {'player_id': 1, 'username': 'XeroX'},
            {'player_id': 2, 'username': 'jay'}
        ],
        data_right=[
            {'game_id': 2, 'player_id': 1, 'score': 17},
            {'game_id': 3, 'player_id': 2, 'score': 22},
            {'game_id': 1, 'player_id': 3, 'score': 9999999}
        ],
        ground_truth=[
            {'player_id': 0, 'username': 'root'},  # no such game
            {'game_id': 1, 'player_id': 3, 'score': 9999999},  # no such player
            {'game_id': 2, 'player_id': 1, 'score': 17, 'username': 'XeroX'},
            {'game_id': 3, 'player_id': 2, 'score': 22, 'username': 'jay'}
        ],
        cmp_keys=('game_id', 'player_id', 'score', 'username'),
        join_data_left_items=(0,),
        join_data_right_items=tuple(),
        join_ground_truth_items=(0,),
    ),
    JoinCase(
        joiner=ops.LeftJoiner(),
        join_keys=('player_id',),
        data_left=[
            {'game_id': 2, 'player_id': 1, 'score': 17},
            {'game_id': 3, 'player_id': 2, 'score': 22},
            {'game_id': 4, 'player_id': 2, 'score': 41},
            {'game_id': 1, 'player_id': 3, 'score': 0}
        ],
        data_right=[
            {'player_id': 0, 'username': 'root'},
            {'player_id': 1, 'username': 'XeroX'},
            {'player_id': 2, 'username': 'jay'}
        ],

        ground_truth=[
            # ignore player 0 with 0 games
            {'game_id': 1, 'player_id': 3, 'score': 0},  # unknown player 3
            {'game_id': 2, 'player_id': 1, 'score': 17, 'username': 'XeroX'},
            {'game_id': 3, 'player_id': 2, 'score': 22, 'username': 'jay'},
            {'game_id': 4, 'player_id': 2, 'score': 41, 'username': 'jay'}
        ],
        cmp_keys=('game_id', 'player_id', 'score', 'username'),
        join_data_left_items=(1, 2),
        join_data_right_items=(2,),
        join_ground_truth_items=(2, 3)
    ),
    JoinCase(
        joiner=ops.RightJoiner(),
        join_keys=('player_id',),
        data_left=[
            {'game_id': 2, 'player_id': 1, 'score': 17},
            {'game_id': 5, 'player_id': 1, 'score': 34},
            {'game_id': 3, 'player_id': 2, 'score': 22},
            {'game_id': 4, 'player_id': 2, 'score': 41},
            {'game_id': 1, 'player_id': 3, 'score': 0}
        ],
        data_right=[
            {'player_id': 0, 'username': 'root'},
            {'player_id': 1, 'username': 'XeroX'},
            {'player_id': 2, 'username': 'jay'}
        ],
        ground_truth=[
            # ignore game with unknown player 3
            {'player_id': 0, 'username': 'root'},  # no games for root
            {'game_id': 2, 'player_id': 1, 'score': 17, 'username': 'XeroX'},
            {'game_id': 3, 'player_id': 2, 'score': 22, 'username': 'jay'},
            {'game_id': 4, 'player_id': 2, 'score': 41, 'username': 'jay'},
            {'game_id': 5, 'player_id': 1, 'score': 34, 'username': 'XeroX'}
        ],
        cmp_keys=('game_id', 'player_id', 'score', 'username'),
        join_data_left_items=(2, 3),
        join_data_right_items=(2,),
        join_ground_truth_items=(2, 3)
    ),
    JoinCase(
        joiner=ops.InnerJoiner(suffix_a='_game', suffix_b='_max'),
        join_keys=('player_id',),
        data_left=[
            {'game_id': 2, 'player_id': 1, 'score': 17},
            {'game_id': 3, 'player_id': 1, 'score': 22},
            {'game_id': 1, 'player_id': 3, 'score': 99}
        ],
        data_right=[
            {'player_id': 1, 'username': 'XeroX', 'score': 400},
            {'player_id': 2, 'username': 'jay', 'score': 451},
            {'player_id': 3, 'username': 'Destroyer', 'score': 999},
        ],
        ground_truth=[
            {'game_id': 1, 'player_id': 3, 'score_game': 99, 'score_max': 999, 'username': 'Destroyer'},
            {'game_id': 2, 'player_id': 1, 'score_game': 17, 'score_max': 400, 'username': 'XeroX'},
            {'game_id': 3, 'player_id': 1, 'score_game': 22, 'score_max': 400, 'username': 'XeroX'}
        ],
        cmp_keys=('game_id', 'player_id', 'score', 'username'),
        join_data_left_items=(0, 1),
        join_data_right_items=(0,),
        join_ground_truth_items=(1, 2)
    )
]


@pytest.mark.parametrize('case', JOIN_CASES)
def test_joiner(case: JoinCase) -> None:
    joiner_data_left_rows = [copy.deepcopy(case.data_left[i]) for i in case.join_data_left_items]
    joiner_data_right_rows = [copy.deepcopy(case.data_right[i]) for i in case.join_data_right_items]
    joiner_ground_truth_rows = [copy.deepcopy(case.ground_truth[i]) for i in case.join_ground_truth_items]

    key_func = _Key(*case.cmp_keys)

    joiner_result = case.joiner(case.join_keys, iter(joiner_data_left_rows), iter(joiner_data_right_rows))
    assert isinstance(joiner_result, tp.Iterator)
    assert sorted(joiner_result, key=key_func) == sorted(joiner_ground_truth_rows, key=key_func)

    result = ops.Join(case.joiner, case.join_keys)(iter(case.data_left), iter(case.data_right))
    assert isinstance(result, tp.Iterator)
    assert sorted(result, key=key_func) == sorted(case.ground_truth, key=key_func)


# ########## HEAVY TESTS WITH MEMORY TRACKING ##########


@pytest.fixture(scope='function')
def baseline_memory() -> tp.Generator[int, None, None]:
    yield _run_watchdog(lambda: time.sleep(0.1), limit=100 * MiB, is_baseline=True)


def _run_watchdog(callback: tp.Callable[[], tp.Any], limit: int, is_baseline: bool) -> int:
    thread = memory_watchdog.MemoryWatchdog(limit=limit, is_baseline=is_baseline)
    thread.start()
    try:
        callback()
    finally:
        thread.stop()
        thread.join()
    return thread.maximum_memory_usage


def run_and_track_memory(callback: tp.Callable[[], tp.Any], limit: int) -> tp.Any:
    process_memory = _run_watchdog(callback, limit=limit, is_baseline=False)
    assert process_memory <= limit


def get_map_data() -> tp.Generator[dict[str, tp.Any], None, None]:
    time.sleep(0.1)  # Some sleep for watchdog catch the memory change
    for _ in range(1000000):
        yield {'data': 'HE.LLO', 'n': 2}


@pytest.mark.parametrize('func_mapper, additional_memory', [
    (ops.DummyMapper(), 1 * MiB),  # Strange memory leap on test start
    (ops.LowerCase(column='data'), 500 * KiB),
    (ops.FilterPunctuation(column='data'), 500 * KiB),
    (ops.Split(column='data', separator='E'), 500 * KiB),
    (ops.Product(columns=['data', 'n'], result_column='prod'), 500 * KiB),
    (ops.Filter(condition=lambda row: row['data'] == 'HE.LLO'), 500 * KiB),
    (ops.Project(columns=['data']), 500 * KiB),
])
def test_heavy_map(func_mapper: ops.Mapper, additional_memory: int, baseline_memory: int) -> None:
    time.sleep(1)
    op = ops.Map(func_mapper)(get_map_data())
    run_and_track_memory(lambda: next(op), baseline_memory + additional_memory)


def test_heavy_split(baseline_memory: int) -> None:
    func_map = ops.Split(column='data', separator='E')
    record = {'data': 'E' * 100500, 'n': 2}
    op = func_map(record)
    run_and_track_memory(lambda: next(op), baseline_memory + 500 * KiB)


def get_reduce_data() -> tp.Generator[dict[str, tp.Any], None, None]:
    for letter in ['a', 'b', 'c', 'ddd']:
        time.sleep(0.1)  # Some sleep for watchdog catch the memory change
        for i in range(305000):
            yield {'key': letter, 'value': i}


@pytest.mark.parametrize('func_reducer, additional_memory', [
    (ops.FirstReducer(), 500 * KiB),
    (ops.TermFrequency(words_column='key'), 500 * KiB),
    (ops.Count(column='key'), 500 * KiB),
    (ops.Sum(column='value'), 500 * KiB),
    (ops.TopN(column='key', n=5000), 2 * MiB),
])
def test_heavy_reduce(func_reducer: ops.Reducer, additional_memory: int, baseline_memory: int) -> None:
    op = ops.Reduce(func_reducer, ('key',))(get_reduce_data())
    run_and_track_memory(lambda: next(op), int(baseline_memory + additional_memory))


@pytest.mark.parametrize('func_joiner, additional_memory', [
    (ops.InnerJoiner(), 100 * MiB),
    (ops.LeftJoiner(), 100 * MiB),
    (ops.RightJoiner(), 100 * MiB)
])
def test_heavy_join(func_joiner: ops.Joiner, additional_memory: int, baseline_memory: int) -> None:
    op = ops.Join(func_joiner, ('key',))(get_reduce_data(), get_reduce_data())
    run_and_track_memory(lambda: next(op), baseline_memory + additional_memory)


def get_complexity_join_data() -> tp.Generator[dict[str, tp.Any], None, None]:
    for n in range(100500):
        yield {'key': n, 'value': n}


@pytest.mark.parametrize('func_joiner', [
    ops.InnerJoiner(),
    ops.LeftJoiner(),
    ops.RightJoiner()
])
def test_complexity_join(func_joiner: ops.Joiner) -> None:
    list(ops.Join(func_joiner, ('key',))(get_complexity_join_data(), get_complexity_join_data()))
