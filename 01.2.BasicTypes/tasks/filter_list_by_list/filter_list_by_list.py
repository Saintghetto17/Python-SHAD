def filter_list_by_list(lst_a: list[int] | range, lst_b: list[int] | range) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    list_res = []
    index_b = 0
    length_b = len(lst_b)
    index_a = 0
    length_a = len(lst_a)
    while index_a < length_a:
        if index_b >= length_b:
            list_res.append(lst_a[index_a])
            index_a = index_a + 1
        else:
            if lst_a[index_a] < lst_b[index_b]:
                list_res.append(lst_a[index_a])
                index_a = index_a + 1
            elif lst_a[index_a] == lst_b[index_b]:
                index_a = index_a + 1
                continue
            else:
                index_b = index_b + 1

    return list_res
