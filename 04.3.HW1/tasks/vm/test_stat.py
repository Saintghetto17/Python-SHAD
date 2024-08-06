import sys

from . import cases
from . import vm_scorer


IDS = [test.name for test in cases.TEST_CASES]
TESTS = [test.text_code for test in cases.TEST_CASES]
SCORER = vm_scorer.Scorer(TESTS)


def test_stat() -> None:
    """
    Shows stat for all passed test cases
    Usage:
        $ pytest test_stat.py::test_stat -s
    """
    vm_scorer.dump_tests_stat(sys.stdout, SCORER)
