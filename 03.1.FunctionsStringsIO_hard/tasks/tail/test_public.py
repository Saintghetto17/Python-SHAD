import dataclasses
import io
from collections import Counter
from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture  # typing

from .tail import tail


@dataclasses.dataclass
class Case:
    content: list[str]
    lines: int
    result: list[str]
    description: str

    def __str__(self) -> str:
        return self.description

    def write_to_file(self, filename: Path) -> None:
        with open(filename, 'w') as f:
            for line in self.content:
                f.write(line + '\n')


TEST_CASES = [
    Case(content=[], lines=10, result=[],
         description='empty_file'),
    Case(content=['first', 'second', 'last'], lines=1, result=['last'],
         description='last_line_requested'),
    Case(content=['first', 'second', 'third'], lines=10, result=['first', 'second', 'third'],
         description='more_lines_requested_than_in_file'),
    Case(content=['first', 'second', 'third'], lines=0, result=[],
         description='no_lines_requested'),
    Case(content=[str(x) * 100 for x in range(1000)], lines=1000, result=[str(x) * 100 for x in range(1000)],
         description='all_lines_requested'),
    Case(content=[str(x) * 1000 for x in range(10000)], lines=10, result=[str(x) * 1000 for x in range(9990, 10000)],
         description='last_10_lines_requested_from_not_so_small_file'),
]


@pytest.mark.parametrize('case', TEST_CASES, ids=str)
def test_tail(case: Case, tmp_path: Path) -> None:
    test_file = tmp_path / 'test.log'
    case.write_to_file(test_file)
    output = io.BytesIO()

    tail(test_file, lines_amount=case.lines, output=output)
    answer = output.getvalue().splitlines()  # universal split handling all the \r\n vs \n

    lines = [line.decode() for line in answer]

    assert lines == case.result


def test_real_log_file() -> None:
    log_file = Path(__file__).parent / 'access.log'
    output = io.BytesIO()

    tail(log_file, lines_amount=100, output=output)
    answer = output.getvalue().splitlines()

    lines = [line.decode() for line in answer]

    ips = Counter(line.split()[3] for line in lines)
    handles = Counter(line.split()[5] for line in lines)

    assert dict(handles) == {
        '/': 50,
        '/static/favicon.png': 37,
        '/api/report': 8,
        '/static/style.css': 4,
        '/signup': 1
    }
    assert dict(ips.most_common(5)) == {
        '195.208.27.165': 58,
        '85.89.127.36': 6,
        '35.204.45.179': 4,
        '37.110.10.238': 4,
        '93.175.28.3': 4
    }


def test_stdout_by_default(capsys: CaptureFixture[str]) -> None:
    log_file = Path(__file__).parent / 'access.log'
    last_line = '[28/Sep/2019:15:57:03 +0000] py.manytask.org 91.228.178.70 "GET / HTTP/1.1" 200 0.130 8337 "0.128"'

    tail(log_file, lines_amount=10)
    # stdout is TextIOWrapper with "universal newlines" enabled
    # so splitting should always be done by \n
    answer = capsys.readouterr().out.split('\n')

    assert answer[-1] == ''
    lines = answer[:-1]

    assert len(lines) == 10
    assert lines[-1] == last_line
