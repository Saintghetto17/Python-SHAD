import dataclasses
import io
import itertools
import typing as tp

import pytest

from .merge_lists_3 import merge


@dataclasses.dataclass
class Case:
    lists: tp.Sequence[tp.Sequence[int]]
    name: str

    def __str__(self) -> str:
        return f'merge_{self.name}'


def make_test_cases() -> tp.Generator[Case, None, None]:
    for i in range(10):
        lists: list[list[int]] = [[] for i in range(i + 1)]

        for j in range(2000):
            basket = j % (i + 1)
            lists[basket].append(j)
        yield Case(lists=lists, name=f"list_{i}")

    yield Case(lists=[], name="list_empty")
    yield Case(lists=[[], [], []], name="list_with_empty_lists")

    for i in range(10):
        lists = [[] for i in range(i + 1)]
        for j in range(2000):
            basket = j // (2000 // (i + 1) + 1)
            lists[basket].append(j)

        yield Case(lists=lists, name=f"list_by_blocks_{i}")

    for i in range(10):
        lists = [[] for i in range(i + 1)]
        for j in range(2000):
            basket = j // (2000 // (i + 1) + 1)
            lists[basket - (basket % 2)].append(j)

        yield Case(lists=lists, name=f"list_by_blocks_with_gaps{i}")


@pytest.mark.parametrize('t', list(make_test_cases()), ids=str)
def test_merge(t: Case) -> None:

    input_streams = [io.BytesIO(b"".join(bytes(f"{value}\n", "utf8") for value in list_)) for list_ in t.lists]
    output_stream = io.BytesIO()

    merge(input_streams, output_stream)

    expected_output = b"".join(bytes(f"{value}\n", "utf8") for value in sorted(itertools.chain(*t.lists)))
    actual_output = output_stream.getvalue()

    if expected_output:
        assert actual_output == expected_output
    else:
        assert actual_output in {b"", b"\n"}
