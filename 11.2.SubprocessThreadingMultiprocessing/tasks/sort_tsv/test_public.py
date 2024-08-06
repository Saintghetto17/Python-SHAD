import dataclasses
import filecmp
import timeit
import typing as tp
from pathlib import Path

import pytest
import testlib

from .sort_tsv import python_sort, util_sort


TESTDATA_DIR = Path(__file__).parent / 'testdata'


###################
# Structure asserts
###################


def test_banned_modules() -> None:
    assert testlib.is_module_imported_hard('subprocess'), 'You should use subprocess'
    assert testlib.is_global_used(util_sort, 'subprocess'), 'You should use subprocess'


###################
# Tests
###################


@dataclasses.dataclass
class Case:
    name: str
    file_out: str
    func: tp.Any


TEST_CASES = [
    Case(name='python', file_out='/tmp/data_sorted_python.tsv', func=python_sort),
    Case(name='util', file_out='/tmp/data_sorted_util.tsv', func=util_sort),
]


@pytest.mark.parametrize('case', TEST_CASES)
def test_sort(case: Case) -> None:
    file_in = TESTDATA_DIR / 'data.tsv'
    file_out = case.file_out

    try:
        # Чтобы посмотреть затраченное время для каждой функции,
        # можно запустить pytest с опцией '-s'
        repeat_count = 3
        t = timeit.timeit(lambda: case.func(file_in, file_out), number=repeat_count) / repeat_count
        print(f'\n{case.name} sorting took {t:.3f}s')

        file_ground_truth = TESTDATA_DIR / 'data_sorted_ground_truth.tsv'
        assert filecmp.cmp(file_ground_truth, file_out)
    finally:
        Path(file_out).unlink(missing_ok=True)
