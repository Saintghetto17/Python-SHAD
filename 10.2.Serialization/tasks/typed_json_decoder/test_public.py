import dataclasses
import typing as tp

import pytest

from decimal import Decimal
from .typed_json_decoder import decode_typed_json


@dataclasses.dataclass
class Case:
    name: str
    json_value: str
    expected: tp.Any

    def __str__(self) -> str:
        return 'test_{}'.format(self.name)


TEST_CASES = [
    Case(
        name='test_list',
        json_value='[1, 2, "__custom_key_type__", {"key": "value"}]',
        expected=[1, 2, '__custom_key_type__', {'key': 'value'}],
    ),
    Case(
        name='test_simple_dict',
        json_value='{"1": "one", "2": "two"}',
        expected={"1": "one", "2": "two"},
    ),
    Case(
        name='test_typed_int_dict',
        json_value='{"1": "one", "2": "two", "__custom_key_type__": "int"}',
        expected={1: "one", 2: "two"},
    ),
    Case(
        name='test_inner_typed_fload_dict',
        json_value='{"coeff_map": {"0.23": "0.55", "0.35": "0.75",  "__custom_key_type__": "float"}}',
        expected={'coeff_map': {0.23: '0.55', 0.35: '0.75'}},
    ),
    Case(
        name='test_inner_typed_decimal_dict',
        json_value='[0, 0, null, {"coeff_map": {"0.23": 0.55, "0.35": 0.75,  "__custom_key_type__": "decimal"}}]',
        expected=[0, 0, None, {'coeff_map': {Decimal("0.23"): 0.55, Decimal("0.35"): 0.75}}],
    ),
]


@pytest.mark.parametrize("test_case", TEST_CASES, ids=str)
def test_typed_json_decoder(test_case: Case) -> None:
    result = decode_typed_json(test_case.json_value)
    assert result == test_case.expected
