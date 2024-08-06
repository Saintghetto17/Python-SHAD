from types import FunctionType
from typing import Any

CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    # parsing function signature-definition
    arg_names: tuple[str, ...] = func.__code__.co_varnames
    bit_mask = bin(func.__code__.co_flags)
    bit_mask_binary = bit_mask[::-1]
    flags: list[int] = []
    res_dict: dict[str, Any] = {}
    len_args = len(args)
    len_kwargs = len(kwargs)
    for i in range(len(bit_mask_binary) - 1):
        if bit_mask_binary[i] != '0':
            flags.append(pow(2, i))
            continue
        flags.append(-1)
        if bit_mask_binary[i] == 'b':
            break
    if flags[2] != CO_VARARGS:
        if flags[3] != CO_VARKEYWORDS:
            if func.__code__.co_argcount == 0:
                if func.__code__.co_kwonlyargcount != 0:
                    if len_args != 0:
                        raise TypeError(ERR_TOO_MANY_POS_ARGS)
                    else:
                        if len_kwargs < func.__code__.co_kwonlyargcount:
                            if func.__kwdefaults__ is None:
                                raise TypeError(ERR_MISSING_KWONLY_ARGS)
                            elif len(func.__kwdefaults__) + len_kwargs < func.__code__.co_kwonlyargcount:
                                raise TypeError(ERR_TOO_MANY_POS_ARGS)
                            else:
                                for e in kwargs.keys():
                                    res_dict[e] = kwargs[e]
                                for e in func.__kwdefaults__.keys():
                                    if e not in kwargs.keys():
                                        res_dict[e] = func.__kwdefaults__[e]
                                return res_dict
                        else:
                            for e in kwargs.keys():
                                if e not in arg_names:
                                    raise TypeError(ERR_MISSING_KWONLY_ARGS)
                                res_dict[e] = kwargs[e]
                            return res_dict

                return {}
            if func.__code__.co_argcount < len_args + len_kwargs:
                for e in kwargs.keys():
                    if e in arg_names:
                        raise TypeError(ERR_MULT_VALUES_FOR_ARG)
                raise TypeError(ERR_TOO_MANY_POS_ARGS)
            elif func.__code__.co_argcount > len_args + len_kwargs:
                if func.__defaults__ is None:
                    raise TypeError(ERR_MISSING_POS_ARGS)
                if func.__code__.co_argcount > len_args + len_kwargs + len(func.__defaults__):
                    raise TypeError(ERR_MISSING_POS_ARGS)
                else:
                    if len_args == 0 and len_kwargs < len(arg_names):
                        if len(func.__defaults__) < len(arg_names):
                            raise TypeError(ERR_MISSING_POS_ARGS)
                        else:
                            if len_args == 0 and len_kwargs == 0:
                                for i in range(len(arg_names)):
                                    res_dict[arg_names[i]] = func.__defaults__[i]
                                return res_dict
                    for i in range(len_args + len(func.__defaults__)):
                        if func.__code__.co_posonlyargcount == 0:
                            if i <= len_args - 1:
                                res_dict[arg_names[i]] = args[i]
                            else:
                                res_dict[arg_names[i]] = func.__defaults__[i - len_args]
                        else:
                            for pos in range(len(func.__defaults__)):
                                if pos < len_args:
                                    res_dict[arg_names[pos]] = args[pos]
                                else:
                                    res_dict[arg_names[pos]] = func.__defaults__[pos]
                            for index in range(len(arg_names)):
                                if index < func.__code__.co_posonlyargcount:
                                    if arg_names[i] in kwargs.keys():
                                        raise TypeError(ERR_POSONLY_PASSED_AS_KW)
                            for kw_key in kwargs.keys():
                                if kw_key in res_dict.keys():
                                    res_dict[kw_key] = kwargs[kw_key]
                            return res_dict
                    for key in kwargs.keys():
                        res_dict[key] = kwargs[key]
                    for e in arg_names:
                        if e not in res_dict.keys():
                            raise TypeError(ERR_MISSING_POS_ARGS)
                    return res_dict
            else:
                arguments: tuple[str, ...] = func.__code__.co_varnames
                pos_only = func.__code__.co_posonlyargcount
                if pos_only == 0:
                    for i in range(len_args):
                        res_dict[arguments[i]] = args[i]
                    if func.__code__.co_argcount > len_args:
                        for e in kwargs.keys():
                            if e not in arg_names:
                                raise TypeError(ERR_MISSING_POS_ARGS)
                            res_dict[e] = kwargs[e]
                    return res_dict
                else:
                    if len_args < pos_only:
                        raise TypeError(ERR_POSONLY_PASSED_AS_KW)
                    for i in range(len_args):
                        res_dict[arguments[i]] = args[i]
                    for e in kwargs.keys():
                        if e in res_dict.keys():
                            raise TypeError(ERR_POSONLY_PASSED_AS_KW)
                        res_dict[e] = kwargs[e]
                    return res_dict
        else:
            if func.__code__.co_posonlyargcount == 0:
                if func.__code__.co_kwonlyargcount == 0:
                    kwargs_name = arg_names[len(arg_names) - 1]
                    res_dict[kwargs_name] = {}
                    for key in kwargs.keys():
                        res_dict[kwargs_name][key] = kwargs[key]
                    return res_dict
                else:
                    kwargs_name = arg_names[len(arg_names) - 1]
                    res_dict[kwargs_name] = {}
                    for e in kwargs.keys():
                        if e not in arg_names:
                            res_dict[kwargs_name][e] = kwargs[e]
                        else:
                            res_dict[e] = kwargs[e]
                    return res_dict

            else:
                if func.__code__.co_kwonlyargcount == 0:
                    kwargs_name = arg_names[len(arg_names) - 1]
                    res_dict[kwargs_name] = {}
                    if len_args < func.__code__.co_posonlyargcount:
                        raise TypeError(ERR_MISSING_POS_ARGS)
                    else:
                        for i in range(len_args):
                            if i < func.__code__.co_posonlyargcount:
                                res_dict[arg_names[i]] = args[i]
                        for e in kwargs.keys():
                            res_dict[kwargs_name][e] = kwargs[e]
                    return res_dict
                else:
                    return {}
    else:
        if flags[3] != CO_VARKEYWORDS:
            var_arg_position = func.__code__.co_argcount
            name_packed = arg_names[var_arg_position]
            res_dict[name_packed] = args
            return res_dict
        else:
            if len_args == 0 and func.__code__.co_posonlyargcount != 0:
                raise TypeError(ERR_MISSING_POS_ARGS)
            kwargs_name = arg_names[len(arg_names) - 1]
            res_dict[kwargs_name] = {}
            var_arg_position = func.__code__.co_argcount
            name_packed = arg_names[len(arg_names) - 2]
            res_dict[name_packed] = []
            for i in range(len(arg_names)):
                if i < var_arg_position:
                    if i < len_args:
                        res_dict[arg_names[i]] = args[i]
                    else:
                        if func.__defaults__ is None:
                            continue
                        else:
                            res_dict[arg_names[i]] = func.__defaults__[i - len_args]
                else:
                    if i < len(arg_names) - 1:
                        if i >= len(args):
                            if i >= len_args:
                                if arg_names[i] in kwargs.keys():
                                    res_dict[arg_names[i]] = kwargs[arg_names[i]]
                        else:
                            res_dict[name_packed].append(args[i])
                            continue
                    if i == len(arg_names) - 1:
                        if i > len_args + len_kwargs:
                            res_dict[kwargs_name] = {}
                        else:
                            j = i
                            for e in kwargs.keys():
                                if e not in res_dict.keys():
                                    if j <= len(arg_names):
                                        res_dict[e] = kwargs[e]
                                        j += 1
                                        continue
                                    res_dict[kwargs_name][e] = kwargs[e]
                                else:
                                    raise TypeError(ERR_MULT_VALUES_FOR_ARG)
            res_dict[name_packed] = tuple(res_dict[name_packed])
            for key in res_dict[kwargs_name].keys():
                if key in res_dict.keys():
                    raise TypeError(ERR_MULT_VALUES_FOR_ARG)
            for key in func.__kwdefaults__.keys():
                if key not in res_dict.keys() and key not in res_dict[kwargs_name].keys():
                    res_dict[key] = func.__kwdefaults__[key]
            for i in range(len(arg_names) - 2):
                if arg_names[i] not in res_dict and arg_names[i] not in res_dict[kwargs_name]:
                    raise TypeError(ERR_MISSING_KWONLY_ARGS)
            return res_dict
