import io
import sys
import traceback
import types
import typing as tp
from contextlib import contextmanager


def compile_code(text_code: types.CodeType | str) -> types.CodeType:
    """
    This is utility function with primary purpose to convert string code to code type.
    Secondary purpose - print byte code for text_code and all nested text_code
    :param text_code: text code for compiling
    :return: compiled code
    """
    if isinstance(text_code, str):
        # print("Text code:\n{}\n".format(text_code))
        # print("Disassembled code:\n")
        # dis.dis(text_code)
        # print("\n")
        code = compile(text_code, '<stdin>', 'exec')
    else:
        code = text_code

    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            compile_code(const)

    # print("Disassembled code co params:\n")
    # print(
    #     "Co consts: {}\nCo freevars: {}\nCo flags: {}\n"
    #     "Co cellvars: {}\nCo kwonlyargcount: {}\nCo names: {}\n"
    #     "Co nlocals: {}\nCo varnames: {}\nCo stacksize: {}\n"
    #     "Co name: {}\nCo lnotab: {}\nCo argcount: {}\n".format(
    #         code.co_consts, code.co_freevars,
    #         code.co_flags,
    #         code.co_cellvars,
    #         code.co_kwonlyargcount,
    #         code.co_names,
    #         code.co_nlocals,
    #         code.co_varnames,
    #         code.co_stacksize,
    #         code.co_name,
    #         list(code.co_lnotab),
    #         code.co_argcount)
    # )

    return code


@contextmanager
def redirected(out: tp.TextIO = sys.stdout, err: tp.TextIO = sys.stderr) -> tp.Iterator[None]:
    """
    Context manage for capturing standart outputs
    :param out: input text stream
    :param err: output text stream
    """
    saved_stdout = sys.stdout
    saved_stderr = sys.stderr
    try:
        sys.stdout = out
        sys.stderr = err
        yield
    finally:
        sys.stdout = saved_stdout
        sys.stderr = saved_stderr


def execute(code: types.CodeType,
            func: tp.Callable[..., None],
            *args: tp.Any) -> tuple[str, str, type[BaseException] | None]:
    """
    Capture all output from function execution
    :param code: code object to calculate
    :param func: functions which
    :param args: any number of arguments appropriate for function call
    :return: tuple of function execution output
    """
    stdout = io.StringIO()
    stderr = io.StringIO()

    exc_type, exc_value, exc_traceback = None, None, None

    with redirected(out=stdout, err=stderr):
        try:
            func(code, *args)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()

    if exc_value:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

    out = stdout.getvalue()
    err = stderr.getvalue()
    return out, err, exc_type
