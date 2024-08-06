import pytest
import time
import typing as tp

from compgraph import operations as ops
from . import memory_watchdog


KiB = 1024
MiB = 1024 * KiB


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
    op = ops.Reduce(func_reducer, ('key', ))(get_reduce_data())
    run_and_track_memory(lambda: next(op), int(baseline_memory + additional_memory))


@pytest.mark.parametrize('func_joiner, additional_memory', [
    (ops.InnerJoiner(), 100 * MiB),
    (ops.LeftJoiner(), 100 * MiB),
    (ops.RightJoiner(), 100 * MiB)
])
def test_heavy_join(func_joiner: ops.Joiner, additional_memory: int, baseline_memory: int) -> None:
    op = ops.Join(func_joiner, ('key', ))(get_reduce_data(), get_reduce_data())
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
    list(ops.Join(func_joiner, ('key', ))(get_complexity_join_data(), get_complexity_join_data()))
