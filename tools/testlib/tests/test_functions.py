from __future__ import annotations

import copy
import types
import typing as tp
from dataclasses import dataclass, field
from inspect import cleandoc

import pytest

from testlib.functions import is_input_unchanged, is_instruction_used, is_regexp_used, is_bytecode_op_used, is_global_used, _get_function_instructions


@dataclass
class FunctionTestCase:
    name: str
    text_code: str
    code: types.CodeType = field(init=False)
    obj: tp.Any = field(init=False)
    object_name: str = 'foo'

    def __post_init__(self) -> None:
        self.text_code = cleandoc(self.text_code)
        self.code = compile(self.text_code, '<string>', 'exec')
        self.obj = self._get_object(self.code, self.object_name)

    @staticmethod
    def _get_object(code: types.CodeType, object_name: str) -> tp.Callable[..., tp.Any]:
        locals_: dict[tp.Any, tp.Any] = {}
        globals_: dict[tp.Any, tp.Any] = {}
        exec(code, globals_, locals_)
        obj = locals_[object_name]
        obj.__globals__.update(globals_)
        obj.__globals__.update(locals_)
        return obj


def test_str_to_object() -> None:
    def foo() -> None:
        a = 1

    foo_str = cleandoc(r"""
        def foo() -> None:
            a = 1
    """)
    foo_compiled = compile(foo_str, '<string>', 'exec')
    foo_obj = FunctionTestCase._get_object(foo_compiled, 'foo')

    foo_instr = [(i.opname, i.argval) for i in _get_function_instructions(foo)]
    obj_instr = [(i.opname, i.argval) for i in _get_function_instructions(foo_obj)]
    assert foo_instr == obj_instr


class TestInput:
    def test_args_changed(self) -> None:
        def _foo(a: list[int], b: dict[str, tp.Any] | None = None) -> None:
            b = b or {}
            b = copy.deepcopy(b)
            a.append(1)
            b['123'] = '123'

        assert not is_input_unchanged(_foo, input_args=([1, 2, 3],))

    def test_kwargs_changed(self) -> None:
        def _foo(a: list[int], b: dict[str, tp.Any] | None = None) -> None:
            b = b or {}
            a = copy.deepcopy(a)
            a.append(1)
            b['123'] = '123'

        assert not is_input_unchanged(_foo, input_args=([1, 2, 3],), input_kwargs={'b': {1: 2}})

    def test_unchanged(self) -> None:
        def _foo(a: list[int], b: dict[str, tp.Any] | None = None) -> None:
            b = b or {}
            a = copy.deepcopy(a)
            b = copy.deepcopy(b)
            a.append(1)
            b['123'] = '123'

        assert is_input_unchanged(_foo, input_args=([1, 2, 3],), input_kwargs={'b': {1: 2}})


@dataclass
class RegexpTestCase(FunctionTestCase):
    used_regexp: set[str] = field(default_factory=set)
    unused_regexp: set[str] = field(default_factory=set)


REGEXP_TEST_CASES: list[RegexpTestCase] = [
    # RegexpTestCase(
    #     name='sorted',
    #     used_regexp={'sorted'},
    #     text_code=r"""
    #         def foo():
    #             sorted([1, 2, 3])
    # """),
    # RegexpTestCase(
    #     name=':=',
    #     used_regexp={':='},
    #     text_code=r"""
    #         def foo():
    #             if (a := 1):
    #                 print(a)
    # """),
    # RegexpTestCase(
    #     name='__.*__',
    #     used_regexp={'__.*__'},
    #     text_code=r"""
    #         def foo():
    #             int.__class__
    # """),
]


class TestRegexp:
    @pytest.mark.parametrize('case', REGEXP_TEST_CASES, ids=[case.name for case in REGEXP_TEST_CASES])
    def test_regexp(self, case: RegexpTestCase) -> None:
        obj = case.obj

        for inst in case.used_regexp:
            assert is_regexp_used(obj, inst)
        for inst in case.unused_regexp:
            assert not is_regexp_used(obj, inst)


@dataclass
class BytecodeOpTestCase(FunctionTestCase):
    used_instructions: set[str] = field(default_factory=set)
    unused_instructions: set[str] = field(default_factory=set)


BYTECODE_OP_TEST_CASES = [
    BytecodeOpTestCase(
        name='empty',
        used_instructions={'RETURN_VALUE'},
        text_code=r"""
            def foo():
                pass
    """),
    BytecodeOpTestCase(
        name='comprehension',
        used_instructions={'BUILD_LIST', 'LOAD_METHOD'},
        text_code=r"""
            def foo():
                t = set() 
                t.add(12)
                a = [1, 2, 3]
    """),
    BytecodeOpTestCase(
        name='in_func',
        used_instructions={'BUILD_LIST', 'LOAD_METHOD'},
        text_code=r"""
            def bar():
                t = set() 
                t.add(12)
                a = [1, 2, 3]
                
            def foo():
                bar()
    """),
    BytecodeOpTestCase(
        name='inner_func',
        used_instructions={'BUILD_LIST', 'LOAD_METHOD'},
        text_code=r"""
            def foo():
                def bar():
                    t = set() 
                    t.add(12)
                    a = [1, 2, 3]
                    
                bar()
    """),
    BytecodeOpTestCase(
        name='in_class_init',
        used_instructions={'BUILD_LIST', 'LOAD_GLOBAL'},
        text_code=r"""
            def t():
                pass 
                
            class A:
                def __init__(self):
                    t = set() 
                    t.add(12)
                    a = [1, 2, 3]
                
            def foo():
                t()
                a = A()
    """),
    BytecodeOpTestCase(
        name='in_class_new',
        used_instructions={'BUILD_LIST', 'LOAD_GLOBAL'},
        text_code=r"""
            def t():
                pass 
                
            class A:
                def __new__(cls):
                    self = super(A, cls).__new__(cls)
                    t = set() 
                    t.add(12)
                    a = [1, 2, 3]
                    return self
                
            def foo():
                t()
                a = A()
    """),
    # BytecodeOpTestCase(
    #     name='in_class_method',
    #     used_instructions={'BUILD_LIST', 'LOAD_METHOD'},
    #     text_code=r"""
    #         class A:
    #             def bar(self):
    #                 t = set()
    #                 t.add(12)
    #                 a = [1, 2, 3]
    #
    #         def foo():
    #             a = A()
    #             a.bar()
    # """),
    # BytecodeOpTestCase(
    #     name='in_other_class_method',
    #     used_instructions={'BUILD_LIST', 'LOAD_METHOD'},
    #     text_code=r"""
    #         class A:
    #             def _bar(self):
    #                 t = set()
    #                 t.add(12)
    #                 a = [1, 2, 3]
    #
    #             def bar(self):
    #                 self._bar()
    #
    #         def foo():
    #             a = A()
    #             a.bar()
    # """),
    # BytecodeOpTestCase(
    #     name='inner_func_in_class_method',
    #     used_instructions={'BUILD_LIST', 'LOAD_METHOD'},
    #     text_code=r"""
    #         class A:
    #             def bar(self):
    #                 def r():
    #                     t = set()
    #                     t.add(12)
    #                     a = [1, 2, 3]
    #
    #                 r()
    #
    #         def foo():
    #             a = A()
    #             a.bar()
    # """),
    # BytecodeOpTestCase(
    #     name='inherited_class_method',
    #     used_instructions={'BUILD_LIST', 'LOAD_METHOD'},
    #     text_code=r"""
    #         class A:
    #             def tmp(self):
    #                 t = set()
    #                 t.add(12)
    #                 a = [1, 2, 3]
    #
    #         class B(A):
    #             pass
    #
    #         def foo():
    #             a = B()
    #             a.bar()
    # """),
    BytecodeOpTestCase(
        name='in_class_not_used_method',
        unused_instructions={'BUILD_LIST', 'LOAD_METHOD'},
        text_code=r"""
            class A:
                def bar(self):
                    a = [1, 2, 3]
                
            def foo():
                a = A()
    """),
    BytecodeOpTestCase(
        name='deep_in_func',
        used_instructions={'BUILD_LIST', 'LIST_EXTEND', 'STORE_FAST', 'LOAD_CONST'},
        unused_instructions={'LOAD_METHOD'},
        text_code=r"""
            def not_used_tmp():
                t = set() 
                t.add(12)
                
            def tmp():
                a = []
                a += [1, 2, 3]
        
            def foobar():
                tmp()
        
            def bar():
                foobar()
                
            def foo():
                bar()
    """),
]


@dataclass
class BuiltinsTestCase(FunctionTestCase):
    used_instructions: set[str] = field(default_factory=set)
    unused_instructions: set[str] = field(default_factory=set)


BUILTINS_TEST_CASES = [
    BuiltinsTestCase(
        name='global_sorted',
        used_instructions={'sorted'},
        text_code=r"""
            def foo():
                sorted([1, 2, 3])
    """),
    BuiltinsTestCase(
        name='global_list_and_set',
        used_instructions={'list', 'set'},
        text_code=r"""
            def foo():
                a = list(1, 2, 3)
                set(a)
    """),
    BuiltinsTestCase(
        name='global_hidden',
        used_instructions={'sorted'},
        text_code=r"""
            def foo():
                s = sorted
                s([1, 2, 3])
    """),
    # BuiltinsTestCase(
    #     name='global_not_builtin',
    #     unused_instructions={'global_staff'},
    #     text_code=r"""
    #         global_staff = 1
    #         def foo():
    #             a = []
    #             a.append(global_staff)
    # """),
    BuiltinsTestCase(
        name='global_globals',
        used_instructions={'globals'},
        unused_instructions={'sorted'},
        text_code=r"""
            def foo():
                s = globals()['sorted']
                s([1, 2, 3])
    """),
    BuiltinsTestCase(
        name='global_builtins',
        used_instructions={'__builtins__'},
        unused_instructions={'sorted'},
        text_code=r"""
            def foo():
                s = __builtins__.__dict__['sorted']
                s([1, 2, 3])
    """),
]


class TestInstructions:
    @pytest.mark.parametrize('case', BYTECODE_OP_TEST_CASES, ids=[case.name for case in BYTECODE_OP_TEST_CASES])
    def test_bytecode_op_used(self, case: BytecodeOpTestCase) -> None:
        obj = case.obj

        print('_get_function_instructions', [(i.opname, i.argval) for i in _get_function_instructions(obj)])
        for inst in case.used_instructions:
            assert is_bytecode_op_used(obj, inst)
        for inst in case.unused_instructions:
            assert not is_bytecode_op_used(obj, inst)

    @pytest.mark.parametrize('case', BUILTINS_TEST_CASES, ids=[case.name for case in BUILTINS_TEST_CASES])
    def test_builtins_used(self, case: BuiltinsTestCase) -> None:
        obj = case.obj

        print([(i.opname, i.argval) for i in _get_function_instructions(obj)])
        for inst in case.used_instructions:
            assert is_global_used(obj, inst)
        for inst in case.unused_instructions:
            assert not is_global_used(obj, inst)



