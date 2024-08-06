def reverse_iterative(lst: list[int]) -> list[int]:
    """
    Return reversed list. You can use only iteration
    :param lst: input list
    :return: reversed list
    """
    lst_res = []
    length = len(lst)
    for i in range(length):
        lst_res.append(lst[length - i - 1])
    return lst_res


def reverse_inplace_iterative(lst: list[int]) -> None:
    """
    Revert list inplace. You can use only iteration
    :param lst: input list
    :return: None
    """
    if (len(lst) == 0):
        return
    index_first = 0
    index_last = len(lst) - 1
    while True:
        temp = lst[index_first]
        lst[index_first] = lst[index_last]
        lst[index_last] = temp
        index_first = index_first + 1
        index_last = index_last - 1
        if index_first == index_last:
            return
        elif index_first >= len(lst) / 2:
            return


def reverse_inplace(lst: list[int]) -> None:
    """
    Revert list inplace with reverse method
    :param lst: input list
    :return: None
    """
    lst.reverse()
    return


def reverse_reversed(lst: list[int]) -> list[int]:
    """
    Revert list with `reversed`
    :param lst: input list
    :return: reversed list
    """
    lst_res = []
    for i in reversed(lst):
        lst_res.append(lst[i - 1])
    return lst_res


def reverse_slice(lst: list[int]) -> list[int]:
    """
    Revert list with slicing
    :param lst: input list
    :return: reversed list
    """
    return lst[-1::-1]
