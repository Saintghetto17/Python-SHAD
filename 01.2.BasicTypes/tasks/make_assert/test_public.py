import pytest
import testlib

from .make_assert import test_check_ctr, ctr_correct_implementation


###################
# Structure asserts
###################


def test_clr_used_in_test() -> None:
    assert testlib.is_global_used(test_check_ctr, 'ctr'), \
        'To test ctf function you should use ctr function'
    assert not testlib.is_global_used(test_check_ctr, 'ctr_correct_implementation'), \
        'Use provided `expected_result` to test, not `ctr_correct_implementation`'


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(test_check_ctr)
    assert testlib.is_function_docstring_exists(ctr_correct_implementation)


###################
# Tests
###################

def test_clicks_equals_shows_not_assert() -> None:
    test_check_ctr(2, 2, 1.0)


def test_zero_shows_not_assert() -> None:
    test_check_ctr(100, 0, 0.0)


def test_zero_clicks_not_assert() -> None:
    test_check_ctr(0, 100, 0.0)


def test_fractional_ctr_assert() -> None:
    with pytest.raises(AssertionError, match="Wrong ctr calculation"):
        test_check_ctr(1, 2, 0.5)


def test_ctr_greater_then_one_assert() -> None:
    with pytest.raises(AssertionError, match="Wrong ctr calculation"):
        test_check_ctr(10, 5, 1.0)


def test_ctr2_clicks_equals_shows() -> None:
    result = ctr_correct_implementation(2, 2)
    assert isinstance(result, float)
    assert result == 1.0


def test_ctr2_zero_shows() -> None:
    result = ctr_correct_implementation(0, 0)
    assert isinstance(result, float)
    assert result == 0.0


def test_ctr2_fractional() -> None:
    result = ctr_correct_implementation(1, 2)
    assert isinstance(result, float)
    assert result == 0.5


def test_ctr2_clicks_greater_than_shows() -> None:
    with pytest.raises(AssertionError, match="Clicks greater than shows"):
        ctr_correct_implementation(2, 1)
