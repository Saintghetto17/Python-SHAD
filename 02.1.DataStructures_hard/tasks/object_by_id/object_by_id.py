import ctypes
import typing as tp


LONG_LEN = 8
INT_LEN = 4
CHAR_LEN = 1

ULONG_CHAR = "L" if ctypes.sizeof(ctypes.c_ulong) == 8 else "Q"
LONG_CHAR = "l" if ctypes.sizeof(ctypes.c_long) == 8 else "q"


def get_object_by_id(object_id: int) -> int | float | tuple[tp.Any, ...] | list[tp.Any] | str | bool:
    """
    Restores object by id.
    :param object_id: Object Id.
    :return: An object that corresponds to object_id.
    """
