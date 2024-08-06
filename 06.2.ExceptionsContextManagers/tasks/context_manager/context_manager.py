import sys
import traceback
from contextlib import contextmanager
from typing import Iterator, TextIO, Type


@contextmanager
def supresser(*types_: Type[BaseException]) -> Iterator[None]:
    try:
        yield
    except types_:
        pass


@contextmanager
def retyper(type_from: Type[BaseException], type_to: Type[BaseException]) -> Iterator[None]:
    try:
        yield
    except type_from:
        bs_ex = sys.exc_info()[1]
        if bs_ex is not None:
            args = bs_ex.args
        raise type_to(*args)


@contextmanager
def dumper(stream: TextIO | None = None) -> Iterator[None]:
    try:
        yield
    except Exception as e:
        if stream is not None:
            lst_new: list[str] = traceback.format_exception_only(type(e), e)
            err_message_new: str = lst_new[len(lst_new) - 1]
            stream.write(err_message_new)
        else:
            lst_old: list[str] = traceback.format_exception_only(type(e), e)
            err_message_old: str = lst_old[len(lst_old) - 1]
            sys.stderr.write(err_message_old)
        raise e
