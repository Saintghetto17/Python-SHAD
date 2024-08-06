import dis
import types
import inspect
import typing as tp
from collections.abc import Callable, Generator
import copy


def is_input_unchanged(
        func: Callable[..., tp.Any],
        input_args: tuple[tp.Any, ...] | None = None,
        input_kwargs: dict[tp.Any, tp.Any] | None = None
) -> bool:
    input_args = input_args or ()
    input_kwargs = input_kwargs or {}

    input_args_copy = copy.deepcopy(input_args)
    input_kwargs_copy = copy.deepcopy(input_kwargs)

    func(*input_args, **input_kwargs)

    return input_args == input_args_copy and input_kwargs == input_kwargs_copy


def is_regexp_used(func: Callable[..., tp.Any], substr: str) -> bool:
    return substr in inspect.getsource(func)


def _extract_global(
        func: Callable[..., tp.Any] | types.CodeType,
        name: str
) -> tp.Callable[..., tp.Any] | None:
    if isinstance(func, types.CodeType):
        return None
    func = tp.cast(types.FunctionType, func)
    some_global = func.__globals__.get(name, None)
    if some_global is not None:
        if isinstance(some_global, types.FunctionType) and not isinstance(some_global, types.BuiltinFunctionType):
            return some_global
    return None


def _get_function_instructions(
        func: Callable[..., tp.Any] | types.CodeType,
        visited_names: set[str] | None = None,
        visited_globals: set[str] | None = None,
        base_func: Callable[..., tp.Any] | types.CodeType | None = None,
        extra_vars: set[str] | None = None,
) -> Generator[dis.Instruction, None, None]:
    # extra_vars = extra_vars or dict()

    if base_func is None:
        assert not isinstance(func, types.CodeType)
        base_func = func

    visited_globals = visited_globals or set()

    # yield from dis.get_instructions(func)
    for inst in dis.get_instructions(func):
        yield inst
        if inst.opname == "LOAD_GLOBAL" and inst.argval not in visited_globals:
            visited_globals.add(inst.argval)
            some_global = _extract_global(base_func, inst.argval)
            if some_global is not None:
                yield from _get_function_instructions(some_global, visited_names, visited_globals, func)

    visited_names = visited_names or set()

    if not isinstance(func, types.CodeType):
        func = tp.cast(types.FunctionType, func)
        # print(f'  func.__code__.co_names {func.__code__.co_names}')
        for name in func.__code__.co_names:
            some_global = func.__globals__.get(name, None)
            # print(f'  try co_names  {name=} {some_global=} {type(some_global)=}')
            if some_global is not None and name not in visited_names:
                visited_names.add(name)
                visited_globals.add(name)

                if isinstance(some_global, types.FunctionType) and \
                        not isinstance(some_global, types.BuiltinFunctionType):
                    yield from _get_function_instructions(some_global, visited_names, visited_globals, func)
                if isinstance(some_global, type):
                    # TODO: class methods
                    # Only for overwrite __init__ and __new__
                    # (otherwise it is 'wrapper_descriptor' or 'builtin_function_or_method')
                    if isinstance(some_global.__init__, types.FunctionType):  # type: ignore
                        yield from _get_function_instructions(
                            some_global.__init__, visited_names, visited_globals, func  # type: ignore
                        )
                    if isinstance(some_global.__new__, types.FunctionType):
                        yield from _get_function_instructions(  # type: ignore
                            some_global.__new__, visited_names, visited_globals, func
                        )
        func_code = func.__code__
    else:
        func_code = func

    for const in func_code.co_consts:
        if isinstance(const, types.CodeType):
            yield from _get_function_instructions(const, visited_names, base_func=base_func)


def is_bytecode_op_used(func: Callable[..., tp.Any], value: str) -> bool:
    return any(
        getattr(instr, 'opname') == value for instr in _get_function_instructions(func)
    )


def is_global_used(func: Callable[..., tp.Any], value: str) -> bool:
    return any(
        getattr(instr, 'opname') == 'LOAD_GLOBAL' and getattr(instr, 'argval') == value
        for instr in _get_function_instructions(func)
    )


def is_instruction_used(func: Callable[..., tp.Any], param: str, value: str | None = None) -> bool:
    # if value is not None:
    return any(
        getattr(instr, param) == value for instr in _get_function_instructions(func)
    )
    # else:
