from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path
from itertools import chain
import uuid

import pytest

from testlib.modules import get_file_imports, get_module_imports


@dataclass
class FileTestCase:
    name: str
    modules: set[str]
    text_code: str

    def __post_init__(self) -> None:
        self.text_code = cleandoc(self.text_code)


FILE_TEST_CASES = [
    FileTestCase(
        name='no_imports',
        modules=set(),
        text_code=r"""
            pass
            print(42)
    """),
    FileTestCase(
        name='direct_import',
        modules={'dataclasses', 'numpy', 'pytest', 'pathlib', 'json', 'inspect', 'importlib'},
        text_code=r"""
            import dataclasses
            import numpy as np
            import pytest, pathlib
            import json.dump
            import inspect, importlib as implib
    """),
    FileTestCase(
        name='from_import',
        modules={'dataclasses', 'pytest', 'pandas', 'numpy', 'itertools'},
        text_code=r"""
            from dataclasses import dataclass
            from pytest import mask, raises
            from pandas import DataFrame as T
            from numpy.arrays import mask
            from itertools import *
    """),
    FileTestCase(
        name='from_local_import',
        modules=set(),
        text_code=r"""
            from . import tester
            from . import utils
            from .checker import check, grade
            from .checker import check as t
    """),
    FileTestCase(
        name='try_import',
        modules={'baconhameggs', 'guido'},
        text_code=r"""
            try:
                import baconhameggs
            except ImportError:
                pass
            
            try:
                import guido.python
            except ImportError:
                pass
    """),
    FileTestCase(
        name='in_function_import',
        modules={'math', 'pickle'},
        text_code=r"""
            def foo():
                import math
                import pickle as pk
    """),
    FileTestCase(
        name='future_import',
        modules={'__future__'},
        text_code=r"""
            from __future__ import (absolute_import, division)
    """),
    FileTestCase(
        name='mesh',
        modules={'bar1', 'bar3', 'bar2', 'sys', 'foo9', 'foo4', 'foo5', 'foo6', 'os', 'foo1', 'foo2', 'foo3'},
        text_code=r"""
            import sys, os
            import foo1
            from foo2 import bar
            from foo3 import bar as che
            import foo4 as boo
            import foo5.zoo
            from foo6 import *
            from . import foo7, foo8
            from .foo12 import foo13
            from foo9 import foo10, foo11
            
            def do():
                import bar1
                from bar2 import foo
                from bar3 import che as baz
    """),
]


class TestImported:
    @pytest.mark.parametrize('case', FILE_TEST_CASES, ids=[i.name for i in FILE_TEST_CASES])
    def test_file(self, case: FileTestCase, tmp_path: Path) -> None:
        tmp_file = tmp_path / 'tmp.py'
        with open(tmp_file, 'w') as f:
            f.write(case.text_code)

        assert get_file_imports(tmp_file) == case.modules

    def test_flat_module(self, tmp_path: Path) -> None:
        for case in FILE_TEST_CASES:
            tmp_file = tmp_path / f'{uuid.uuid1()}.py'

            with open(tmp_file, 'w') as f:
                f.write(case.text_code)

        test_cases_modules = [case.modules for case in FILE_TEST_CASES]
        assert get_module_imports(tmp_path) == set(chain.from_iterable(test_cases_modules))

    def test_deep_module(self, tmp_path: Path) -> None:
        current_tmp_path = tmp_path
        for case in FILE_TEST_CASES:
            tmp_file = current_tmp_path / f'{uuid.uuid1()}.py'

            with open(tmp_file, 'w') as f:
                f.write(case.text_code)

            current_tmp_path = current_tmp_path / f'{uuid.uuid1()}'
            current_tmp_path.mkdir()

        test_cases_modules = [case.modules for case in FILE_TEST_CASES]
        assert get_module_imports(tmp_path) == set(chain.from_iterable(test_cases_modules))
