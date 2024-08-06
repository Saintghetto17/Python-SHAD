# mypy: ignore-errors

import inspect
import tempfile
import typing as tp

import mypy.api

from . import typy_protocol
from .typy_protocol import get


def check_annotations(func):
    for p, value in inspect.signature(func).parameters.items():
        if p == "self":
            assert value.annotation == inspect.Signature.empty, f"Parameter {p} should not have annotation"
        else:
            assert value.annotation != inspect.Signature.empty, f"Parameter {p} does not have annotation"
            assert value.annotation != tp.Any, f"Parameter {p} has prohibited Any annotation"

    assert inspect.signature(func).return_annotation != inspect.Signature.empty, "Return does not have annotation"
    assert inspect.signature(func).return_annotation != tp.Any, "Return has prohibited Any annotation"


def check_func(module, test_case, is_success):
    with tempfile.NamedTemporaryFile(mode="w") as fp:
        fp.write("import typing as tp")
        fp.write("\n")
        fp.write("import numbers")
        fp.write("\n")
        fp.write("import abc")
        fp.write("\n\n")
        fp.write(inspect.getsource(module))
        fp.write("\n")
        fp.write(inspect.getsource(test_case))
        fp.write("\n")
        fp.flush()

        normal_report, error_report, exit_status = mypy.api.run([fp.name, '--config-file', ''])
        print(f"Report:\n{normal_report}\n{error_report}")
        result_success_status = exit_status == 0

        assert result_success_status is is_success, \
            f"Mypy check should be {is_success}, but result {result_success_status}"


def case1() -> None:
    class A:
        def __init__(self, a: str):
            self._a = a

        def __getitem__(self, item: int) -> str:
            return self._a[item]

        def __len__(self) -> int:
            return len(self._a)

    get(A("hello"), 4)


def case2() -> None:
    class A:
        def __init__(self, a: str):
            self._a = a

        def __getitem__(self, item: int) -> str:
            return self._a[item]

    get(A("hello"), 4)


def case3() -> None:
    class A:
        def __getitem__(self, item: int) -> bool:
            return True

        def __len__(self) -> int:
            return 0

    get(A(), 4)


def test_protocol() -> None:

    check_annotations(get)

    check_func(typy_protocol, case1, True)
    check_func(typy_protocol, case2, False)
    check_func(typy_protocol, case3, True)
