"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import collections.abc
import dis
import operator
import types
import typing as tp

CO_VARARGS = 4
CO_VARKEYWORDS = 8


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.11/Include/frameobject.h

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.return_value = None
        # index of last attempted instruction in bytecode
        self.f_lasti = 0
        self.dict_instructions: dict[int, int] = {}
        self.last_exception = None
        self.kwname: dict[int, str] | None = None
        self.arg: int = 0

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def load_assertion_error_op(self, none: tp.Any) -> None:
        self.push(AssertionError)

    def raise_varargs_op(self, flag: int) -> None:
        if flag == 1:
            self.push(self.pop())
        elif flag == 2:
            err = self.pop()
            err.__cause__ = self.pop()
            self.push(err)

    def run(self) -> tp.Any:
        instructions = list(dis.get_instructions(self.code))
        length = len(instructions)
        # collect all instructions in map to make jumps
        for i in range(length):
            self.dict_instructions[instructions[self.f_lasti].offset] = (
                self.f_lasti)
            self.f_lasti += 1
        self.f_lasti = 0
        # run instructions
        while self.f_lasti < length:
            if instructions[self.f_lasti].opname == 'RETURN_VALUE':
                getattr(self, instructions[self.f_lasti].opname.lower()
                        + "_op")(
                    instructions[self.f_lasti].argval)
                break
            self.f_lasti += 1
            (getattr(self, instructions[self.f_lasti - 1].opname.lower()
                     + "_op")
             (instructions[self.f_lasti - 1].argval))
        return self.return_value

    def jump_if_true_or_pop_op(self, delta: int) -> None:
        TOS = self.top()
        if TOS is True:
            self.f_lasti = self.dict_instructions[delta]
        else:
            self.pop()

    def jump_if_false_or_pop_op(self, delta: int) -> None:
        TOS = self.top()
        if TOS is False:
            self.f_lasti = self.dict_instructions[delta]
        else:
            self.pop()

    def pop_jump_forward_if_false_op(self, delta: int) -> None:
        TOS = self.top()
        if TOS is False:
            self.f_lasti = self.dict_instructions[delta]
        self.pop()

    def unpack_sequence_op(self, count: int) -> None:
        TOS = self.pop()
        tpl: tuple[tp.Any] = TOS
        for e in tpl:
            self.push(e)

    def resume_op(self, arg: int) -> tp.Any:
        pass

    def push_null_op(self, arg: int) -> tp.Any:
        self.push(None)

    def precall_op(self, arg: int) -> tp.Any:
        pass

    def call_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-CALL
        """
        # positional + named arguments are popped
        arguments = self.popn(arg)
        # self or callable
        optional = self.pop()
        # if self
        if not hasattr(optional, '__call__'):
            # pop the callable
            func = self.pop()
            self.push(func(optional, *arguments))
        # if callable
        else:
            try:
                # pop the NULL statement after
                # self (second var according to docs)
                second = self.pop()
                if second is not None:
                    self.push(second)
            except Exception:
                pass
            # optional is callable
            self.push(optional(*arguments))

    def jump_backward_op(self, delta: int) -> None:
        self.f_lasti = self.dict_instructions[delta]

    def jump(self, jump: int) -> None:
        self.f_lasti = self.dict_instructions[jump]

    COMPARE_OPERATORS = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge
    }

    def compare_op_op(self, op: str) -> None:
        lhs = self.pop()
        rhs = self.pop()
        self.push(self.COMPARE_OPERATORS[op](rhs, lhs))

    BINARY_OPERATORS = {
        0: operator.add,
        1: operator.and_,
        2: operator.floordiv,
        3: operator.lshift,
        4: operator.matmul,
        5: operator.mul,
        6: operator.mod,
        7: operator.or_,
        8: operator.pow,
        9: operator.rshift,
        10: operator.sub,
        11: operator.truediv,
        12: operator.xor,
        13: operator.add,
        14: operator.and_,
        15: operator.floordiv,
        16: operator.lshift,
        17: operator.matmul,
        18: operator.mul,
        19: operator.mod,
        20: operator.or_,
        21: operator.pow,
        22: operator.rshift,
        23: operator.sub,
        24: operator.truediv,
        25: operator.xor
    }

    def unary_positive_op(self, nothing: tp.Any) -> None:
        pass

    def unary_negative_op(self, nothing: tp.Any) -> None:
        el = self.pop()
        self.push(-el)

    def unary_not_op(self, nothing: tp.Any) -> None:
        el = self.pop()
        self.push(not el)

    def unary_invert_op(self, nothing: tp.Any) -> None:
        el = self.pop()
        self.push(~el)

    def is_op_op(self, invert: int) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        self.push(TOS1)
        self.push(TOS)
        if invert != 1:
            self.push(TOS is TOS1)
        else:
            self.push(TOS is not TOS1)

    def delete_fast_op(self, var_num: tp.Any) -> None:
        pass

    def delete_name_op(self, namei: str) -> None:
        del self.locals[namei]

    def delete_subscr_op(self, nothing: tp.Any) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        del TOS1[TOS]
        self.push(TOS1)
        self.push(TOS)

    def store_subscr_op(self, nothing: tp.Any) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        TOS2 = self.pop()
        TOS1[TOS] = TOS2
        self.push(TOS1)
        self.push(TOS)

    def binary_subscr_op(self, nothing: tp.Any) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        self.push(TOS1[TOS])

    def build_slice_op(self, argc: int) -> None:
        if argc == 2:
            TOS = self.pop()
            TOS1 = self.pop()
            res = slice(TOS1, TOS)
            self.push(res)
        elif argc == 3:
            TOS = self.pop()
            TOS1 = self.pop()
            TOS2 = self.pop()
            res = slice(TOS2, TOS1, TOS)
            self.push(res)

    def contains_op_op(self, invert: int) -> None:
        if invert != 1:
            collection = self.pop()
            el = self.pop()
            if el in collection:
                self.push(True)
            else:
                self.push(False)
        else:
            collection = self.pop()
            el = self.pop()
            if el not in collection:
                self.push(True)
            else:
                self.push(False)

    def store_fast_op(self, name: str) -> None:
        TOS = self.pop()
        self.locals[name] = TOS

    def load_method_op(self, method: tp.Any) -> None:
        self.push(getattr(self.pop(), method, None))

    def load_fast_op(self, name: str) -> None:
        if name in self.locals:
            value = self.locals[name]
        else:
            raise UnboundLocalError("local variable "
                                    "'%s' referenced before assignment" % name)
        self.push(value)

    def build_const_key_map_op(self, count: int) -> None:
        keys: tuple[tp.Any] = self.pop()
        map_res: dict[tp.Any, tp.Any] = {}
        values: tuple[tp.Any] = self.popn(count)
        for i in range(count):
            map_res[keys[i]] = values[i]
        self.push(map_res)

    def build_map_op(self, count: int) -> None:
        res_dict: dict[tp.Any, tp.Any] = {}
        for i in range(count):
            if len(self.data_stack) == 0:
                break
            TOS = self.pop()
            TOS1 = self.pop()
            res_dict[TOS1] = TOS
        self.push(res_dict)

    def unpack_ex_op(self, counts: int) -> None:
        pass

    def extended_arg_op(self, ext: tp.Any) -> None:
        pass

    def list_extend_op(self, i: int) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        TOS1.extend(TOS)
        self.push(TOS1)

    def dict_update_op(self, i: int) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        TOS1.update(TOS)
        self.push(TOS1)

    def set_update_op(self, i: int) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        TOS1.update(TOS)
        self.push(TOS1)

    def list_to_tuple_op(self, nothing: tp.Any) -> None:
        TOS = self.pop()
        self.push(tuple(TOS))

    def build_tuple_op(self, count: int) -> None:
        lst: list[tp.Any] = []
        for i in range(count):
            el = self.pop()
            lst.append(el)
        lst_res: list[tp.Any] = []
        for i in range(count):
            lst_res.append(lst[count - 1 - i])
        self.push(tuple(lst_res))

    def build_set_op(self, count: int) -> None:
        st: set[tp.Any] = set()
        for i in range(count):
            el = self.pop()
            st.add(el)
        self.push(st)

    def swap_op(self, i: int) -> None:
        if i == len(self.data_stack):
            item1 = self.pop()
            item2 = self.pop()
            self.push(item1)
            self.push(item2)
            return None
        item = self.data_stack[i - 1]
        TOS = self.pop()
        try:
            self.data_stack[i - 1] = TOS
        except Exception:
            self.push(TOS)
        self.push(item)

    def copy_op(self, i: int) -> None:
        index = self.pop()
        lst = self.pop()
        lst[index] += [i]
        self.push(lst)

    def set_add_op(self, i: int) -> None:
        TOS = self.pop()
        TOS1 = self.data_stack[0]
        TOS1.add(TOS)

    def map_add_op(self, i: int) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        dct = self.data_stack[0]
        dct[TOS1] = TOS

    def list_append_op(self, i: int) -> None:
        TOS = self.pop()
        TOS1 = self.data_stack[0]
        TOS1.append(TOS)

    def build_list_op(self, count: int) -> None:
        lst: list[tp.Any] = []
        for i in range(count):
            el = self.pop()
            lst.append(el)
        lst_res: list[tp.Any] = []
        for i in range(count):
            lst_res.append(lst[count - 1 - i])
        self.push(lst_res)

    def load_attr_op(self, namei: str) -> None:
        to_replace = self.pop()
        self.push(getattr(to_replace, namei))

    def import_star_op(self, name: str) -> None:
        # import
        mod = self.pop()
        # dir gives us all attributes from import
        for attr in dir(mod):
            if attr[0] != '_':
                self.locals[attr] = getattr(mod, attr)

    def import_name_op(self, namei: str) -> None:
        lvl, fromlist = self.popn(2)
        self.push(__import__(namei, self.globals,
                             self.locals, fromlist, level=lvl))

    def import_from_op(self, namei: str) -> None:
        mod = self.top()
        self.push(getattr(mod, namei))

    def load_build_class_op(self, nothing: tp.Any) -> None:
        self.push(builtins.__build_class__)

    def binary_op_op(self, op: int) -> None:
        lhs = self.pop()
        rhs = self.pop()
        if rhs is None:
            rhs = ""
        # NOTE 21!!!
        if op == 8 or op == 21:
            self.push(rhs ** lhs)
            return None
        self.push(self.BINARY_OPERATORS[op](rhs, lhs))

    def get_len_op(self, nothing: tp.Any) -> None:
        TOS = self.top()
        self.push(len(TOS))

    def build_string_op(self, count: int) -> None:
        res = ''
        index = 0
        for e in self.data_stack[-count:]:
            index += 1
            if isinstance(e, str):
                res = res + str(e)
                continue
            self.pop()
            res = res + e
        self.push(res)

    def get_iter_op(self, jump: int) -> None:
        # puts iterator on TOS
        self.push(iter(self.pop()))

    def format_value_op(self, flags: int) -> None:
        self.push(str(self.pop()))

    def for_iter_op(self, jump: int) -> None:
        # get the iterator from TOS
        top_iter = self.top()
        try:
            # put the next value of iterator on TOS
            v = next(top_iter)
            self.push(v)
        except StopIteration:
            # pop iterator
            self.pop()
            # jump to another instruction
            self.jump(jump)

    def return_generator_op(self, nothing: tp.Any) -> None:
        pass

    def pop_jump_backward_if_true_op(self, delta: int) -> None:
        if self.pop():
            self.jump(delta)

    def pop_jump_backward_if_false_op(self, delta: int) -> None:
        if not self.pop():
            self.jump(delta)

    def match_mapping_op(self, nothing: int) -> None:
        if isinstance(self.top(), collections.abc.Mapping):
            self.push(True)
        else:
            self.push(False)

    def match_sequence_op(self, nothing: int) -> None:
        if isinstance(self.top(), collections.abc.Sequence):
            self.push(True)
        else:
            self.push(False)

    def match_keys_op(self, nothing: tp.Any) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        flag = False
        for key in TOS:
            if key not in TOS1.keys():
                flag = True
                break
        if flag:
            self.push(None)
        else:
            self.push(tuple(TOS1.values()))

    def pop_except(self, ex: tp.Any) -> None:
        self.pop()

    def pop_jump_forward_if_not_none_op(self, delta: int) -> None:
        TOS = self.top()
        if TOS is not None:
            self.f_lasti = self.dict_instructions[delta]
        self.pop()

    def pop_jump_forward_if_none_op(self, delta: int) -> None:
        TOS = self.top()
        if TOS is None:
            self.f_lasti = self.dict_instructions[delta]
        self.pop()

    def kw_names_op(self, i: int) -> None:
        pass

    def jump_forward_op(self, delta: int) -> None:
        self.f_lasti = self.dict_instructions[delta]

    def pop_jump_forward_if_true_op(self, delta: int) -> None:
        if self.top():
            self.f_lasti = self.dict_instructions[delta]
        # TOS is popped regardless the condition above
        self.pop()

    def load_name_op(self, arg: str) -> None:
        """
        Partial realization

        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-LOAD_NAME
        """
        # TODO: parse all scopes
        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise NameError

    def delete_global_op(self, namei: str) -> None:
        del self.globals[namei]

    def load_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-LOAD_GLOBAL
        """
        # TODO: parse all scopes
        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise NameError

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-LOAD_CONST
        """
        self.push(arg)

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-RETURN_VALUE
        """
        self.return_value = self.pop()

    def before_with_op(self, delta: int) -> None:
        pass

    def dict_merge_op(self, i: int) -> None:
        TOS = self.pop()
        TOS1 = self.pop()
        TOS1.update(TOS)
        self.push(TOS1)

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-POP_TOP
        """
        self.pop()

    def call_function_ex_op(self, flags: int) -> None:
        pass

    def deleting_local_names_op(self, name: str) -> None:
        pass

    def store_attr_op(self, namei: str) -> None:
        val, obj = self.popn(2)
        setattr(obj, namei, val)

    def delete_attr_op(self, namei: str) -> None:
        delattr(self.pop(), namei)

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-MAKE_FUNCTION
        """
        code = self.pop()  # the code associated with the function (at TOS1)

        # TODO: use arg to parse function defaults

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments
            #  using code attributes such as co_argcount
            parsed_args: dict[str, tp.Any] = {}
            parsed_args = dict.fromkeys(code.co_varnames, args)
            ind = 0
            if len(args) == 0:
                for key in parsed_args.keys():
                    parsed_args[key] = []
                    ind += 1
            index = 0
            for key in parsed_args.keys():
                if index >= len(args):
                    break
                parsed_args[key] = args[index]
                index += 1
            parsed_args.update(kwargs)
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)
            frame = Frame(code, self.builtins, self.globals, f_locals)
            # Run code in prepared environment
            return frame.run()

        self.push(f)

    def nop_op(self, nth: tp.Any) -> None:
        pass

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.11.5/library/dis.html#opcode-STORE_NAME
        """
        const = self.pop()
        self.locals[arg] = const

    def store_global_op(self, arg: str) -> None:
        const_global = self.pop()
        self.globals[arg] = const_global


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'],
                      globals_context, globals_context)
        return frame.run()
