import time
import typing as tp
from itertools import islice, cycle
from operator import itemgetter

import pytest
from pytest import approx

from compgraph import algorithms, operations
from . import memory_watchdog


MiB = 1024 ** 2


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


def run_and_track_memory(callback: tp.Callable[[], tp.Any], limit: int) -> None:
    process_memory = _run_watchdog(callback, limit=limit, is_baseline=False)
    assert process_memory <= limit


def test_yandex_maps_heavy(baseline_memory: int) -> None:
    graph = algorithms.yandex_maps_graph(
        'travel_time', 'edge_length',
        enter_time_column='enter_time', leave_time_column='leave_time', edge_id_column='edge_id',
        start_coord_column='start', end_coord_column='end',
        weekday_result_column='weekday', hour_result_column='hour', speed_result_column='speed'
    )

    lengths = [
        {'start': [37.84870228730142, 55.73853974696249], 'end': [37.8490418381989, 55.73832445777953],
         'edge_id': 8414926848168493057},
        {'start': [37.524768467992544, 55.88785375468433], 'end': [37.52415172755718, 55.88807155843824],
         'edge_id': 5342768494149337085},
        {'start': [37.56963176652789, 55.846845586784184], 'end': [37.57018438540399, 55.8469259692356],
         'edge_id': 5123042926973124604},
        {'start': [37.41463478654623, 55.654487907886505], 'end': [37.41442892700434, 55.654839486815035],
         'edge_id': 5726148664276615162},
        {'start': [37.584684155881405, 55.78285809606314], 'end': [37.58415022864938, 55.78177368734032],
         'edge_id': 451916977441439743},
        {'start': [37.736429711803794, 55.62696328852326], 'end': [37.736344216391444, 55.626937723718584],
         'edge_id': 7639557040160407543},
        {'start': [37.83196756616235, 55.76662947423756], 'end': [37.83191015012562, 55.766647034324706],
         'edge_id': 1293255682152955894},
    ]

    times = [
        {'leave_time': '20171020T112238.723000', 'enter_time': '20171020T112237.427000',
         'edge_id': 8414926848168493057},
        {'leave_time': '20171011T145553.040000', 'enter_time': '20171011T145551.957000',
         'edge_id': 8414926848168493057},
        {'leave_time': '20171020T090548.939000', 'enter_time': '20171020T090547.463000',
         'edge_id': 8414926848168493057},
        {'leave_time': '20171024T144101.879000', 'enter_time': '20171024T144059.102000',
         'edge_id': 8414926848168493057},
        {'leave_time': '20171022T131828.330000', 'enter_time': '20171022T131820.842000',
         'edge_id': 5342768494149337085},
        {'leave_time': '20171014T134826.836000', 'enter_time': '20171014T134825.215000',
         'edge_id': 5342768494149337085},
        {'leave_time': '20171010T060609.897000', 'enter_time': '20171010T060608.344000',
         'edge_id': 5342768494149337085},
        {'leave_time': '20171027T082600.201000', 'enter_time': '20171027T082557.571000',
         'edge_id': 5342768494149337085}
    ]

    expected = [
        {'weekday': 'Fri', 'hour': 8, 'speed': approx(62.2322, 0.001)},
        {'weekday': 'Fri', 'hour': 9, 'speed': approx(78.1070, 0.001)},
        {'weekday': 'Fri', 'hour': 11, 'speed': approx(88.9552, 0.001)},
        {'weekday': 'Sat', 'hour': 13, 'speed': approx(100.9690, 0.001)},
        {'weekday': 'Sun', 'hour': 13, 'speed': approx(21.8577, 0.001)},
        {'weekday': 'Tue', 'hour': 6, 'speed': approx(105.3901, 0.001)},
        {'weekday': 'Tue', 'hour': 14, 'speed': approx(41.5145, 0.001)},
        {'weekday': 'Wed', 'hour': 14, 'speed': approx(106.4505, 0.001)}
    ]

    def graph_run() -> tp.Iterator[operations.TRow]:
        return iter(graph.run(travel_time=lambda: islice(cycle(iter(times)), len(times) * 10000),
                              edge_length=lambda: iter(lengths)))

    def it_graph() -> None:
        for _ in graph_run():
            pass

    run_and_track_memory(
        lambda: it_graph(),
        int(baseline_memory + 20 * MiB)
    )

    assert expected == sorted(graph_run(), key=itemgetter('weekday', 'hour'))
