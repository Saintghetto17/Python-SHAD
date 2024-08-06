# mypy: ignore-errors

import inspect
import tempfile
import typing as tp

import mypy.api

from . import typy_generic
from .typy_generic import Pair


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


def test_pair():
    p = Pair[int](1, 2)
    assert p.first() == 1
    assert p.second() == 2
    assert p.sum() == 3

    p += Pair[int](3, 4)
    assert p.first() == 4
    assert p.second() == 6
    assert p.sum() == 10


def case1() -> None:
    Pair[int](1, 2.0)  # fail


def case2() -> None:
    Pair[int](1.0, 2)  # fail


def case3() -> None:
    Pair[int](1, 2)  # success


def case4() -> None:
    Pair[float](1.0, 2.0)  # success


def case5() -> None:
    Pair[float](1, 2)  # success


def case6() -> None:
    Pair[str]("a", "b")  # fail


def test_func5() -> None:
    check_annotations(Pair.first)
    check_annotations(Pair.second)
    check_annotations(Pair.sum)
    check_annotations(Pair.__init__)
    check_annotations(Pair.__iadd__)

    check_func(typy_generic, case1, False)
    check_func(typy_generic, case2, False)
    check_func(typy_generic, case3, True)
    check_func(typy_generic, case4, True)
    check_func(typy_generic, case5, True)
    check_func(typy_generic, case6, False)
