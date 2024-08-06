import heapq
import typing as tp
from collections import deque


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    sum = 0
    heap: list[deque[int]] = []
    for stream in input_streams:
        deq_ints: deque[int] = deque()
        val = stream.readline()
        while val != b'':
            number = int(val)
            deque.append(deq_ints, number)
            val = stream.readline()
        if len(deq_ints) == 0:
            continue
        sum = sum + len(deq_ints)
        heapq.heappush(heap, deq_ints)
    for i in range(sum):
        deq_pop: deque[int] = heapq.heappop(heap)
        value = deq_pop.popleft()
        output_stream.write(str(value).encode('utf-8'))
        term_n = b'\n'
        output_stream.write(term_n)
        if len(deq_pop) == 0:
            continue
        heapq.heappush(heap, deq_pop)
