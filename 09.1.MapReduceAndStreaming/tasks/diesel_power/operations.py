import copy
import heapq
import re
import string
import sys
from abc import abstractmethod, ABC
import typing as tp
from itertools import groupby

TRow = dict[str, tp.Any]
TRowsIterable = tp.Iterable[TRow]
TRowsGenerator = tp.Generator[TRow, None, None]


class Operation(ABC):
    @abstractmethod
    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass


class Read(Operation):
    def __init__(self, filename: str, parser: tp.Callable[[str], TRow]) -> None:
        self.filename = filename
        self.parser = parser

    def __call__(self, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        with open(self.filename) as f:
            for line in f:
                yield self.parser(line)


class ReadIterFactory(Operation):
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for row in kwargs[self.name]():
            yield row


# Operations


class Mapper(ABC):
    """Base class for mappers"""

    @abstractmethod
    def __call__(self, row: TRow) -> TRowsGenerator:
        """
        :param row: one table row
        """
        pass


class Map(Operation):
    def __init__(self, mapper: Mapper) -> None:
        self.mapper = mapper

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for row in rows:
            yield from self.mapper(row)


class Reducer(ABC):
    """Base class for reducers"""

    @abstractmethod
    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        """
        :param rows: table rows
        """
        pass


class Reduce(Operation):
    def __init__(self, reducer: Reducer, keys: tp.Sequence[str]) -> None:
        self.reducer = reducer
        self.keys = keys

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        key: str = self.keys[0]
        for key_group, grouped_row in groupby(rows, key=lambda row: row[key]):
            yield from self.reducer(tuple(self.keys), grouped_row)


class Joiner(ABC):
    """Base class for joiners"""

    def __init__(self, suffix_a: str = '_1', suffix_b: str = '_2') -> None:
        self._a_suffix = suffix_a
        self._b_suffix = suffix_b

    @abstractmethod
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        """
        :param keys: join keys
        :param rows_a: left table rows
        :param rows_b: right table rows
        """
        pass


class Join(Operation):
    def __init__(self, joiner: Joiner, keys: tp.Sequence[str]):
        self.keys = keys
        self.joiner = joiner

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        key: str = self.keys[0]
        flag_empty_1: bool = False
        flag_empty_2: bool = False
        iter_pairs_1: tp.Iterator[tuple[tp.Any, tp.Iterator[TRow]]] = groupby(rows, key=lambda row: row[key])
        iter_pairs_2: tp.Iterator[tuple[tp.Any, tp.Iterator[TRow]]] = groupby(args[0], key=lambda row: row[key])
        key_stream_1, grouped_stream_1 = next(iter_pairs_1)
        key_stream_2, grouped_stream_2 = next(iter_pairs_2)
        while not flag_empty_1 or not flag_empty_2:
            if key_stream_2 > key_stream_1:
                if not isinstance(self.joiner, InnerJoiner) and not isinstance(self.joiner, RightJoiner):
                    yield from self.joiner(self.keys, grouped_stream_1, iter({}))
                try:
                    key_stream_1, grouped_stream_1 = next(iter_pairs_1)
                except StopIteration:
                    flag_empty_1 = True
                    key_stream_1 = sys.maxsize
                else:
                    continue
            elif key_stream_2 < key_stream_1:
                if not isinstance(self.joiner, InnerJoiner) and not isinstance(self.joiner, LeftJoiner):
                    yield from self.joiner(self.keys, iter({}), grouped_stream_2)
                try:
                    key_stream_2, grouped_stream_2 = next(iter_pairs_2)
                except StopIteration:
                    flag_empty_2 = True
                    key_stream_2 = sys.maxsize
                else:
                    continue
            elif key_stream_2 == key_stream_1:
                yield from self.joiner(self.keys, grouped_stream_1, grouped_stream_2)
                try:
                    key_stream_1, grouped_stream_1 = next(iter_pairs_1)
                except StopIteration:
                    flag_empty_1 = True
                    key_stream_1 = sys.maxsize
                    try:
                        key_stream_2, grouped_stream_2 = next(iter_pairs_2)
                    except StopIteration:
                        break
                    else:
                        continue
                else:
                    try:
                        key_stream_2, grouped_stream_2 = next(iter_pairs_2)
                    except StopIteration:
                        flag_empty_2 = True
                        key_stream_2 = sys.maxsize
                    else:
                        continue


# Dummy operators


class DummyMapper(Mapper):
    """Yield exactly the row passed"""

    def __call__(self, row: TRow) -> TRowsGenerator:
        yield row


class FirstReducer(Reducer):
    """Yield only first row from passed ones"""

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        for row in rows:
            yield row
            break


# Mappers


class FilterPunctuation(Mapper):
    """Left only non-punctuation symbols"""

    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.column] = row[self.column].translate(str.maketrans('', '', string.punctuation))
        yield row


class LowerCase(Mapper):
    """Replace column value with value in lower case"""

    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    @staticmethod
    def _lower_case(txt: str) -> str:
        return txt.lower()

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.column] = self._lower_case(row[self.column])
        yield row


class Split(Mapper):
    """Split row on multiple rows by separator"""

    def __init__(self, column: str, separator: str | None = None) -> None:
        """
        :param column: name of column to split
        :param separator: string to separate by
        """
        self.column = column
        self.separator = separator

    def __call__(self, row: TRow) -> TRowsGenerator:
        reg_str: str = ''
        if self.separator is not None:
            reg_str = self.separator + '+'
        else:
            reg_str = r'\s+'
        reg_ex = re.compile(reg_str)
        last_end: int = 0
        final_row: TRow = dict()
        for token in re.finditer(reg_ex, row[self.column]):
            final_row = copy.deepcopy(row)
            final_row.update({self.column: row[self.column][last_end:token.start()]})
            last_end = token.end()
            yield final_row
        if len(row[self.column]) != last_end:
            final_row = copy.deepcopy(row)
            final_row.update({self.column: row[self.column][last_end:len(row[self.column])]})
            yield final_row


class Product(Mapper):
    """Calculates product of multiple columns"""

    def __init__(self, columns: tp.Sequence[str], result_column: str = 'product') -> None:
        """
        :param columns: column names to product
        :param result_column: column name to save product in
        """
        self.columns = columns
        self.result_column = result_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        final_row: TRow = copy.deepcopy(row)
        product: float = 1
        for elem in self.columns:
            product = product * final_row[elem]
        final_row[self.result_column] = product
        yield final_row


class Filter(Mapper):
    """Remove records that don't satisfy some condition"""

    def __init__(self, condition: tp.Callable[[TRow], bool]) -> None:
        """
        :param condition: if condition is not true - remove record
        """
        self.condition = condition

    def __call__(self, row: TRow) -> TRowsGenerator:
        cond_res: bool = self.condition(row)
        if cond_res:
            yield row


class Project(Mapper):
    """Leave only mentioned columns"""

    def __init__(self, columns: tp.Sequence[str]) -> None:
        """
        :param columns: names of columns
        """
        self.columns = columns

    def __call__(self, row: TRow) -> TRowsGenerator:
        final_row: TRow = copy.deepcopy(row)
        for key in row.keys():
            if key not in self.columns:
                final_row.pop(key)
        yield final_row


# Reducers


class TopN(Reducer):
    """Calculate top N by value"""

    def __init__(self, column: str, n: int) -> None:
        """
        :param column: column name to get top by
        :param n: number of top values to extract
        """
        self.column_max = column
        self.n = n

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        sorted_list = heapq.nlargest(self.n, rows, key=lambda row: row[self.column_max])
        for i in range(self.n):
            yield sorted_list[len(list(rows)) - i - 1]


class TermFrequency(Reducer):
    """Calculate frequency of values in column"""

    def __init__(self, words_column: str, result_column: str = 'tf') -> None:
        """
        :param words_column: name for column with words
        :param result_column: name for result column
        """
        self.words_column = words_column
        self.result_column = result_column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        dct: dict[str, int] = dict()
        sum: int = 0
        remember_group_key: dict[str, tp.Any] = {}
        flag: bool = True
        for row in rows:
            if flag:
                for key in group_key:
                    remember_group_key[key] = row[key]
                flag = False
            if row[self.words_column] not in dct.keys():
                dct[row[self.words_column]] = 1
                sum += 1
                continue
            dct[row[self.words_column]] += 1
            sum += 1
        for elem in dct:
            res_row = {self.words_column: elem, self.result_column: dct[elem] / sum}
            res_row.update(remember_group_key)
            yield res_row


class Count(Reducer):
    """
    Count records by key
    Example for group_key=('a',) and column='d'
        {'a': 1, 'b': 5, 'c': 2}
        {'a': 1, 'b': 6, 'c': 1}
        =>
        {'a': 1, 'd': 2}
    """

    def __init__(self, column: str) -> None:
        """
        :param column: name for result column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        sum: int = 0
        flag: bool = True
        res: dict[str, tp.Any] = {}
        for row in rows:
            if flag:
                for key in group_key:
                    res[key] = row[key]
                flag = False
            sum += 1
        res.update({self.column: sum})
        yield res


class Sum(Reducer):
    """
    Sum values aggregated by key
    Example for key=('a',) and column='b'
        {'a': 1, 'b': 2, 'c': 4}
        {'a': 1, 'b': 3, 'c': 5}
        =>
        {'a': 1, 'b': 5}
    """

    def __init__(self, column: str) -> None:
        """
        :param column: name for sum column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        summary: int = 0
        res: TRow = {}
        first_step: bool = True
        for row in rows:
            summary += row[self.column]
            if first_step:
                for i in range(len(group_key)):
                    res.update({group_key[i]: row[group_key[i]]})
                first_step = False
        res.update({self.column: summary})
        yield res

    # Joiners


class InnerJoiner(Joiner):
    """Join with inner strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        mem_row_a = list(rows_a)
        lst_keys_1 = mem_row_a[0].keys()
        same_keys: list[str] = list()
        first_step: bool = True
        for dct_2 in rows_b:
            if first_step:
                for key in dct_2.keys():
                    if key in lst_keys_1 and key not in keys:
                        same_keys.append(key)
                first_step = False
                for i in range(len(mem_row_a)):
                    for key_change in same_keys:
                        mem_row_a[i].update({key_change + self._a_suffix: mem_row_a[i][key_change]})
                        del mem_row_a[i][key_change]
            for dct_1 in mem_row_a:
                dct_new_2 = copy.deepcopy(dct_2)
                for key_to_change in same_keys:
                    dct_new_2.update({key_to_change + self._b_suffix: dct_new_2[key_to_change]})
                    del dct_new_2[key_to_change]
                dct_new_2.update(dct_1)
                yield dct_new_2


class OuterJoiner(Joiner):
    """Join with outer strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        mem_rem_b = list(rows_b)
        check_in: bool = True
        for row_a in rows_a:
            check_in = False
            if len(mem_rem_b) == 0:
                yield row_a
                continue
            for row_b in mem_rem_b:
                row_a.update(row_b)
                yield row_a
        if check_in:
            for el in mem_rem_b:
                yield el


class LeftJoiner(Joiner):
    """Join with left strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:

        mem_rem_b = list(rows_b)
        for row_a in rows_a:
            if len(mem_rem_b) == 0:
                yield row_a
                continue
            for row_b in mem_rem_b:
                new_row_a = copy.deepcopy(row_a)
                new_row_a.update(row_b)
                yield new_row_a


class RightJoiner(Joiner):
    """Join with right strategy"""

    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        mem_rem_a = list(rows_a)
        for row_b in rows_b:
            if len(mem_rem_a) == 0:
                yield row_b
                continue
            for row_a in mem_rem_a:
                new_row_b = copy.deepcopy(row_b)
                new_row_b.update(row_a)
                yield new_row_b
