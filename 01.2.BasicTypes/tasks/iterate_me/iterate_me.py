def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    list_res = []
    for e in elements:
        list_res.append(e ** 2)
    return list_res


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    size = len(elements)
    indexes = []
    for i in range(size):
        indexes.append(i + 1)
    return indexes


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """

    if len(elements) == 0:
        return None

    else:
        max = elements[0] - 10
        index = 0
        for i in range(len(elements)):
            if elements[i] > max:
                max = elements[i]
                index = i
            # elif elements[i] == max:
            # return None
            else:
                continue
    return index


# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    lst = []
    for i in range(len(elements)):
        if i % 2 != 0:
            lst.append(elements[i])
    return lst


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    index = -1
    for i in range(len(elements)):
        if elements[i] == 3:
            index = i
            return i
    if index < 0:
        return None

    return 0

# ====================================================================================================


def get_last_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    index = -1
    for i in range(len(elements)):
        if elements[i] == 3:
            index = i

    if index < 0:
        return None
    else:
        return index


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)


# ====================================================================================================


def get_min_max(elements: list[int], default: int | None) -> tuple[int | None, int | None]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    if len(elements) == 0:
        return (default, default)
    else:
        return (min(elements), max(elements))


# ====================================================================================================

def get_by_index(elements: list[int], i: int, boundary: int) -> int | None:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    return res if (res := elements[i]) > boundary else None
