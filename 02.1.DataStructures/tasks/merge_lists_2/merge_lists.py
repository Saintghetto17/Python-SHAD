import heapq
import typing as tp


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    res: list[int] = []
    heap_lists: list[list[int]] = []
    sum = 0
    for e in seq:
        cast_to_list = list(e)
        if len(e) == 0:
            sum = sum + 1
            heapq.heappush(heap_lists, cast_to_list)
            continue
        sum = sum + len(e)
        heapq.heappush(heap_lists, cast_to_list)
    for i in range(sum):
        lst: list[int] = heapq.heappop(heap_lists)
        if len(lst) == 0:
            continue
        val = lst[0]
        res.append(val)
        lst.remove(val)
        if len(lst) == 0:
            continue
        heapq.heappush(heap_lists, lst)
    return res
