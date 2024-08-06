import typing as tp

from multiprocessing import Pipe, Process, connection
from operator import itemgetter

from . import operations as ops


def do_sort(endpoint: connection.Connection, keys: tuple[str, ...]) -> None:
    rows = []
    while True:
        row = endpoint.recv()
        if row is None:
            break
        rows.append(row)
    rows.sort(key=itemgetter(*keys))
    for row in rows:
        endpoint.send(row)
    endpoint.send(None)


class ExternalSort(ops.Operation):
    """
    In order to not account materialization during sorting in main process memory consumption, we delegate
    sorting to a separate process.
    This class illustrates cross-process streaming.
    """

    def __init__(self, keys: tp.Sequence[str]):
        self.keys = keys

    def __call__(self, rows: ops.TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> ops.TRowsGenerator:
        local_endpoint, remote_endpoint = Pipe()
        process = Process(target=do_sort, args=(remote_endpoint, self.keys))
        process.start()
        row_count_before = 0
        for row in rows:
            local_endpoint.send(row)
            row_count_before += 1
        local_endpoint.send(None)
        row_count_after = 0
        while True:
            local_endpoint_row = local_endpoint.recv()
            if local_endpoint_row is None:
                break
            yield local_endpoint_row
            row_count_after += 1
        assert row_count_before == row_count_after
        process.join()
