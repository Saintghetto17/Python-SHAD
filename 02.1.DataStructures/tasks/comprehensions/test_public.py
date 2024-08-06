import copy
import dis
import types
import typing as tp

import testlib

from . import comprehensions as comp
from collections.abc import Callable


###################
# Structure asserts
###################


def _is_comprehension(instruction: dis.Instruction, comp_name: str) -> bool:
    return isinstance(instruction.argval, types.CodeType) and instruction.argval.co_name == comp_name


def _is_functional_call(instruction: dis.Instruction) -> bool:
    return instruction.opname == 'LOAD_GLOBAL' and instruction.argval in {'map', 'filter'}


def assert_comprehension_structure(func: Callable[..., tp.Any], comprehension_name: str) -> None:
    is_used_comprehension = any(
        _is_comprehension(i, comprehension_name) for i in testlib.functions._get_function_instructions(func)
    )
    assert is_used_comprehension, "You should use comprehension"

    is_used_functional_call = any(_is_functional_call(i) for i in testlib.functions._get_function_instructions(func))
    assert not is_used_functional_call, "You shouldn't use map/filter functions"

    is_used_loop = any(i.opname == 'SETUP_LOOP' for i in testlib.functions._get_function_instructions(func))
    assert not is_used_loop, "You shouldn't use loops"


def test_get_unique_page_ids_structure() -> None:
    assert not testlib.is_global_used(comp.get_unique_page_ids, 'list')
    assert not testlib.is_global_used(comp.get_unique_page_ids, 'set')
    assert_comprehension_structure(comp.get_unique_page_ids, '<setcomp>')


def test_get_unique_page_ids_visited_after_ts_structure() -> None:
    assert not testlib.is_global_used(comp.get_unique_page_ids_visited_after_ts, 'list')
    assert not testlib.is_global_used(comp.get_unique_page_ids_visited_after_ts, 'set')
    assert_comprehension_structure(comp.get_unique_page_ids_visited_after_ts, '<setcomp>')


def test_get_unique_user_ids_visited_page_after_ts_structure() -> None:
    assert not testlib.is_global_used(comp.get_unique_user_ids_visited_page_after_ts, 'list')
    assert not testlib.is_global_used(comp.get_unique_user_ids_visited_page_after_ts, 'set')
    assert_comprehension_structure(comp.get_unique_user_ids_visited_page_after_ts, '<setcomp>')


def test_get_events_by_device_type_structure() -> None:
    assert not testlib.is_global_used(comp.get_events_by_device_type, 'list')
    assert not testlib.is_global_used(comp.get_events_by_device_type, 'set')
    assert_comprehension_structure(comp.get_events_by_device_type, '<listcomp>')


def test_get_region_ids_with_none_replaces_by_default_structure() -> None:
    assert not testlib.is_global_used(comp.get_region_ids_with_none_replaces_by_default, 'list')
    assert not testlib.is_global_used(comp.get_region_ids_with_none_replaces_by_default, 'set')
    assert_comprehension_structure(comp.get_region_ids_with_none_replaces_by_default, '<listcomp>')


def test_get_region_id_if_not_none_structure() -> None:
    assert not testlib.is_global_used(comp.get_region_id_if_not_none, 'list')
    assert not testlib.is_global_used(comp.get_region_id_if_not_none, 'set')
    assert_comprehension_structure(comp.get_region_id_if_not_none, '<listcomp>')


def test_get_keys_where_value_is_not_none_structure() -> None:
    assert not testlib.is_global_used(comp.get_keys_where_value_is_not_none, 'list')
    assert not testlib.is_global_used(comp.get_keys_where_value_is_not_none, 'set')
    assert_comprehension_structure(comp.get_keys_where_value_is_not_none, '<listcomp>')


def test_get_record_with_none_if_key_not_in_keys_structure() -> None:
    assert not testlib.is_global_used(comp.get_record_with_none_if_key_not_in_keys, 'dict')
    assert_comprehension_structure(comp.get_record_with_none_if_key_not_in_keys, '<dictcomp>')


def test_get_record_with_key_in_keys_structure() -> None:
    assert not testlib.is_global_used(comp.get_record_with_key_in_keys, 'dict')
    assert_comprehension_structure(comp.get_record_with_key_in_keys, '<dictcomp>')


def test_get_keys_if_key_in_keys_structure() -> None:
    assert not testlib.is_global_used(comp.get_keys_if_key_in_keys, 'list')
    assert not testlib.is_global_used(comp.get_keys_if_key_in_keys, 'set')
    assert_comprehension_structure(comp.get_keys_if_key_in_keys, '<setcomp>')


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(comp.get_events_by_device_type)
    assert testlib.is_function_docstring_exists(comp.get_keys_if_key_in_keys)
    assert testlib.is_function_docstring_exists(comp.get_keys_where_value_is_not_none)
    assert testlib.is_function_docstring_exists(comp.get_record_with_key_in_keys)
    assert testlib.is_function_docstring_exists(comp.get_record_with_none_if_key_not_in_keys)
    assert testlib.is_function_docstring_exists(comp.get_region_id_if_not_none)
    assert testlib.is_function_docstring_exists(comp.get_region_ids_with_none_replaces_by_default)
    assert testlib.is_function_docstring_exists(comp.get_unique_page_ids)
    assert testlib.is_function_docstring_exists(comp.get_unique_page_ids_visited_after_ts)
    assert testlib.is_function_docstring_exists(comp.get_unique_user_ids_visited_page_after_ts)


###################
# Tests
###################


TEST_RECORDS: list[tp.Mapping[str, tp.Any]] = [
    {"EventID": 12345, "EventTime": 1568839214, "UserID": 12456,
     "PageID": 10, "RegionID": None, "DeviceType": "Safari"},
    {"EventID": 12346, "EventTime": 1568839215, "UserID": 12456, "PageID": 10, "RegionID": None,
     "DeviceType": "Safari"},
    {"EventID": 12347, "EventTime": 1568839216, "UserID": 12456, "PageID": 11, "RegionID": None,
     "DeviceType": "Safari"},
    {"EventID": 25647, "EventTime": 1568839217, "UserID": 12395, "PageID": 112, "RegionID": 10,
     "DeviceType": "Internet Explorer"},
    {"EventID": 12345, "EventTime": 1568839218, "UserID": 12395, "PageID": 221, "RegionID": 0,
     "DeviceType": "Firefox"},
    {"EventID": 15789, "EventTime": 1568839219, "UserID": 12399, "PageID": 221, "RegionID": 20,
     "DeviceType": "Internet Explorer"},
]


TEST_RECORD: tp.Mapping[str, tp.Any] = TEST_RECORDS[0]


def test_get_unique_page_ids() -> None:
    test_records = copy.deepcopy(TEST_RECORDS)
    result = comp.get_unique_page_ids(test_records)

    assert test_records == TEST_RECORDS, "You shouldn't change inputs"
    assert result == {10, 11, 112, 221}


def test_get_unique_page_ids_visited_after_ts() -> None:
    test_records = copy.deepcopy(TEST_RECORDS)
    result = comp.get_unique_page_ids_visited_after_ts(test_records, 1568839216)

    assert test_records == TEST_RECORDS, "You shouldn't change inputs"
    assert result == {112, 221}


def test_get_unique_user_ids_visited_page_after_ts() -> None:
    test_records = copy.deepcopy(TEST_RECORDS)
    result = comp.get_unique_user_ids_visited_page_after_ts(test_records, 1568839216, 221)

    assert test_records == TEST_RECORDS, "You shouldn't change inputs"
    assert result == {12395, 12399}


def test_get_events_by_device_type() -> None:
    test_records = copy.deepcopy(TEST_RECORDS)
    result = comp.get_events_by_device_type(test_records, "Internet Explorer")

    assert test_records == TEST_RECORDS, "You shouldn't change inputs"
    assert result == [
        {"EventID": 25647, "EventTime": 1568839217, "UserID": 12395, "PageID": 112, "RegionID": 10,
         "DeviceType": "Internet Explorer"},
        {"EventID": 15789, "EventTime": 1568839219, "UserID": 12399, "PageID": 221, "RegionID": 20,
         "DeviceType": "Internet Explorer"}
    ]


def test_get_region_ids_with_none_replaces_by_default() -> None:
    test_records = copy.deepcopy(TEST_RECORDS)
    result = comp.get_region_ids_with_none_replaces_by_default(test_records)

    assert test_records == TEST_RECORDS, "You shouldn't change inputs"
    assert result == [100500, 100500, 100500, 10, 0, 20]


def test_get_region_id_if_not_none() -> None:
    test_records = copy.deepcopy(TEST_RECORDS)
    result = comp.get_region_id_if_not_none(test_records)

    assert test_records == TEST_RECORDS, "You shouldn't change inputs"
    assert result == [10, 0, 20]


def test_get_keys_where_value_is_not_none() -> None:
    test_r = copy.deepcopy(TEST_RECORD)
    result = comp.get_keys_where_value_is_not_none(test_r)

    assert test_r == TEST_RECORD, "You shouldn't change inputs"
    assert sorted(result) == sorted(["EventID", "EventTime", "UserID", "PageID", "DeviceType"])


def test_get_record_with_none_if_key_not_in_keys() -> None:
    test_r = copy.deepcopy(TEST_RECORD)
    result = comp.get_record_with_none_if_key_not_in_keys(test_r, {"EventID", "UserID"})

    assert test_r == TEST_RECORD, "You shouldn't change inputs"
    assert result == {
        "EventID": 12345, "EventTime": None, "UserID": 12456, "PageID": None, "RegionID": None, "DeviceType": None
    }


def test_get_record_with_key_in_keys() -> None:
    test_r = copy.deepcopy(TEST_RECORD)
    result = comp.get_record_with_key_in_keys(test_r, {"EventID", "UserID"})

    assert test_r == TEST_RECORD, "You shouldn't change inputs"
    assert result == {"EventID": 12345, "UserID": 12456}


def test_get_keys_if_key_in_keys() -> None:
    test_r = copy.deepcopy(TEST_RECORD)
    result = comp.get_keys_if_key_in_keys(test_r, {"EventID", "UserID", "SomeField"})

    assert test_r == TEST_RECORD, "You shouldn't change inputs"
    assert result == {"EventID", "UserID"}
