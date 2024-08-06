import inspect
import types
import typing as tp


class FunctionTypeMeta(type):
    _functype = types.FunctionType

    def __instancecheck__(self, instance: tp.Any) -> bool:
        return isinstance(instance, self._functype)


class FunctionTypeBan(metaclass=FunctionTypeMeta):
    _functype = types.FunctionType

    def __new__(cls, *args: tp.Any, **kwargs: tp.Any):  # type: ignore
        filename = inspect.stack()[1].filename
        if filename.endswith('/vm.py'):
            raise RuntimeError('FunctionType is banned in HW1!')
        return cls._functype(*args, **kwargs)


types.FunctionType = FunctionTypeBan  # type: ignore # noqa
