import copy

import testlib

from .iterate_me import get_squares, get_indices_from_one, get_max_element_index, \
    get_every_second_element, get_first_three_index, get_last_three_index, get_sum, get_min_max, \
    get_by_index


###################
# Structure asserts
###################


def test_get_squares_structure() -> None:
    assert testlib.is_bytecode_op_used(get_squares, 'BINARY_OP')


def test_get_sum_structure() -> None:
    assert testlib.is_global_used(get_sum, 'sum')


def test_get_min_max_structure() -> None:
    assert testlib.is_global_used(get_min_max, 'min')
    assert testlib.is_global_used(get_min_max, 'max')


def test_get_by_index_structure() -> None:
    assert testlib.is_regexp_used(get_by_index, ':=')


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(get_by_index)
    assert testlib.is_function_docstring_exists(get_min_max)
    assert testlib.is_function_docstring_exists(get_sum)
    assert testlib.is_function_docstring_exists(get_last_three_index)
    assert testlib.is_function_docstring_exists(get_first_three_index)
    assert testlib.is_function_docstring_exists(get_every_second_element)
    assert testlib.is_function_docstring_exists(get_max_element_index)
    assert testlib.is_function_docstring_exists(get_squares)
    assert testlib.is_function_docstring_exists(get_indices_from_one)


###################
# Tests
###################


def test_get_squares() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    given_list_a = copy.deepcopy(lst_a)

    assert get_squares(lst_a) == [4, 0, 25, 4, 9, 16, 9]

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_squares_empty_list() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_squares(given_list_a) == []

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_indices() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    given_list_a = copy.deepcopy(lst_a)

    assert get_indices_from_one(given_list_a) == [1, 2, 3, 4, 5, 6, 7]

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_indices_empty_list() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_indices_from_one(given_list_a) == []

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_max_element_index() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    given_list_a = copy.deepcopy(lst_a)

    assert get_max_element_index(given_list_a) == 2

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_max_element_index_empty_list() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_max_element_index(given_list_a) is None

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_every_second_element() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    given_list_a = copy.deepcopy(lst_a)

    assert get_every_second_element(given_list_a) == [0, 2, 4]

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_every_second_element_empty_input() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_every_second_element(given_list_a) == []

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_every_second_element_one_element() -> None:
    lst_a = [1]
    given_list_a = copy.deepcopy(lst_a)

    assert get_every_second_element(given_list_a) == []

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_first_three_index() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    given_list_a = copy.deepcopy(lst_a)

    assert get_first_three_index(given_list_a) == 4

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_first_three_index_empty_input() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_first_three_index(given_list_a) is None

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_first_three_index_without_three() -> None:
    lst_a = [-2, 0, 5, 2]
    given_list_a = copy.deepcopy(lst_a)

    assert get_first_three_index(given_list_a) is None

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_last_three_index() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    given_list_a = copy.deepcopy(lst_a)

    assert get_last_three_index(given_list_a) == 6

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_last_three_index_empty_input() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_last_three_index(given_list_a) is None

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_last_three_index_without_three() -> None:
    lst_a = [-2, 0, 5, 2]
    given_list_a = copy.deepcopy(lst_a)

    assert get_last_three_index(given_list_a) is None

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_last_three_index_on_first_position() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    given_list_a = copy.deepcopy(lst_a)

    assert get_last_three_index(given_list_a) == 0

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_sum() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    given_list_a = copy.deepcopy(lst_a)

    assert get_sum(given_list_a) == 21

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_sum_with_empty_input() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_sum(given_list_a) == 0

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_min_max() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    given_list_a = copy.deepcopy(lst_a)

    assert get_min_max(given_list_a, 0) == (0, 6)

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_min_max_with_empty_input_and_zero_default() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_min_max(given_list_a, 0) == (0, 0)

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_min_max_with_empty_input_and_none_default() -> None:
    lst_a: list[int] = []
    given_list_a = copy.deepcopy(lst_a)

    assert get_min_max(given_list_a, None) == (None, None)

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_by_index() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    given_list_a = copy.deepcopy(lst_a)

    assert get_by_index(given_list_a, 5, 3) == 4

    assert given_list_a == lst_a, "You shouldn't change input"


def test_get_by_index_returns_none() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    given_list_a = copy.deepcopy(lst_a)

    assert get_by_index(given_list_a, 5, 4) is None

    assert given_list_a == lst_a, "You shouldn't change input"
