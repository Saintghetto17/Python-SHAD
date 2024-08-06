import math
from collections.abc import Iterable, Iterator, Sized


class RangeIterator(Iterator[int]):
    """The iterator class for Range"""

    def __init__(self, range_: 'Range') -> None:
        self._range = range_
        self.current_index = 0

    def __iter__(self) -> 'RangeIterator':
        return self

    def __next__(self) -> int:
        if self.current_index >= self._range.__len__():
            raise StopIteration
        value = self._range.__getitem__(self.current_index)
        self.current_index += 1
        return value


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        :param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """
        self._stop: int = 0
        self._start: int = 0
        self._step: int = 0
        if len(args) == 1:
            self._start = 0
            self._stop = args[0]
            self._step = 1
        elif len(args) == 2:
            self._start = args[0]
            self._stop = args[1]
            self._step = 1
        elif len(args) == 3:
            if args[2] == 0:
                raise ValueError
            self._start = args[0]
            self._stop = args[1]
            self._step = args[2]

    def __iter__(self) -> 'RangeIterator':
        return RangeIterator(self)

    def __repr__(self) -> str:
        return f"Range({self._start}, {self._stop}, {self._step})"

    def __str__(self) -> str:
        if self._step == 1:
            return f"range({self._start}, {self._stop})"
        return f"range({self._start}, {self._stop}, {self._step})"

    def __contains__(self, key: int) -> bool:
        return abs(self._start - key) % abs(self._step) == 0 and max(self._start, self._stop) >= key >= min(
            self._start, self._stop)

    def __getitem__(self, key: int) -> int:
        if key < 0 or key >= self.__len__():
            raise IndexError(key)
        return self._start + key * self._step

    def __len__(self) -> int:
        if self._step >= 1 and self._start > self._stop:
            return 0
        elif self._step <= -1 and self._start < self._stop:
            return 0
        else:
            return math.ceil(abs((self._stop - self._start)) / abs(self._step))
