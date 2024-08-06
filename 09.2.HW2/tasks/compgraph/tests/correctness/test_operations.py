import copy
import dataclasses
import typing as tp

import pytest
from pytest import approx

from compgraph import operations as ops


class _Key:
    def __init__(self, *args: str) -> None:
        self._items = args

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
        mapper=ops.Product(columns=['speed', 'time'], result_column='distance'),
        data=[
            {'test_id': 1, 'speed': 5, 'time': 10},
            {'test_id': 2, 'speed': 60, 'time': 2},
            {'test_id': 3, 'speed': 3, 'time': 15},
            {'test_id': 4, 'speed': 100, 'time': 0.5},
            {'test_id': 5, 'speed': 48, 'time': 15},
        ],
        ground_truth=[
            {'test_id': 1, 'speed': 5, 'time': 10, 'distance': 50},
            {'test_id': 2, 'speed': 60, 'time': 2, 'distance': 120},
            {'test_id': 3, 'speed': 3, 'time': 15, 'distance': 45},
            {'test_id': 4, 'speed': 100, 'time': 0.5, 'distance': 50},
            {'test_id': 5, 'speed': 48, 'time': 15, 'distance': 720},
        ],
        cmp_keys=('test_id', 'speed', 'time', 'distance')
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
            {'id': 1, 'name': 'a'},
            {'id': 1, 'name': 'b'},
        ],
        data_right=[
            {'id': 1, 'score': 1},
            {'id': 1, 'score': 2},
        ],
        ground_truth=[
            {'id': 1, 'name': 'a', 'score': 1},
            {'id': 1, 'name': 'b', 'score': 1},
            {'id': 1, 'name': 'a', 'score': 2},
            {'id': 1, 'name': 'b', 'score': 2},
        ],
        cmp_keys=('id', 'name', 'score'),
        join_data_left_items=(0, 1),
        join_data_right_items=(0, 1),
        join_ground_truth_items=(0, 1, 2, 3)
    ),
    JoinCase(
        joiner=ops.InnerJoiner(),
        join_keys=(),
        data_left=[
            {'name': 'a'},
            {'name': 'b'},
        ],
        data_right=[
            {'score': 1},
            {'score': 2},
        ],
        ground_truth=[
            {'name': 'a', 'score': 1},
            {'name': 'b', 'score': 1},
            {'name': 'a', 'score': 2},
            {'name': 'b', 'score': 2},
        ],
        cmp_keys=('name', 'score'),
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
