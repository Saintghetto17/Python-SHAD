import typing as tp
import time
from types import TracebackType


class TimeoutException(Exception):
    pass


class HardTimeoutException(TimeoutException):
    """HardTimeOut"""


class SoftTimeoutException(TimeoutException):
    """SoftTimeOut"""


class TimeCatcher:
    def __init__(self, soft_timeout: float | None = None, hard_timeout: float | None = None):
        if soft_timeout is not None and hard_timeout is not None:
            assert soft_timeout > 0 and hard_timeout > 0
            assert soft_timeout <= hard_timeout
        if soft_timeout is None and hard_timeout is not None:
            assert hard_timeout > 0
        if soft_timeout is not None and hard_timeout is None:
            assert soft_timeout > 0
        self.soft_timeout = soft_timeout
        self.hard_timeout = hard_timeout
        self.start_time: float = float(time.time())
        self.consumed: float = 0

    def __enter__(self) -> tp.Self:
        return self

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> bool | None:
        # if we catched some exception after deleting resource
        # at the end of context manager field
        if self.soft_timeout is not None:
            if time.time() - self.start_time > self.soft_timeout:
                raise SoftTimeoutException
        if self.hard_timeout is not None:
            if time.time() - self.start_time > self.hard_timeout:
                raise HardTimeoutException
        if exc_value is not None:
            return True
        return None

    def __float__(self) -> float:
        self.consumed = float(time.time()) - self.start_time
        return self.consumed

    def __str__(self) -> str:
        return 'Time consumed: {time}'.format(time=self.consumed)
