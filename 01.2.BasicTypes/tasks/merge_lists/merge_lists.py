def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    lst_res = []
    ptr_a = 0
    ptr_b = 0
    while True:
        if ptr_a < len(lst_a) and ptr_b < len(lst_b):
            if lst_a[ptr_a] <= lst_b[ptr_b]:
                lst_res.append(lst_a[ptr_a])
                ptr_a = ptr_a + 1
            else:
                lst_res.append(lst_b[ptr_b])
                ptr_b = ptr_b + 1
        else:
            if (ptr_a < len(lst_a) and ptr_b >= len(lst_b)):
                lst_res.append(lst_a[ptr_a])
                ptr_a = ptr_a + 1
            elif (ptr_a >= len(lst_a) and ptr_b < len(lst_b)):
                lst_res.append(lst_b[ptr_b])
                ptr_b = ptr_b + 1
            else:
                return lst_res


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list using `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    lst_res = []
    for a in lst_a:
        lst_res.append(a)
    for b in lst_b:
        lst_res.append(b)
    return sorted(lst_res)
