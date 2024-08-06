import dis
import types


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    res_dict: dict[str, int] = {}
    lst_instructions: list[dis.Instruction] = list(dis.get_instructions(source_code))
    index = 0
    for e in lst_instructions:
        index = index + 1
        operation = e.opname
        type_arg = type(e.argval)
        if type_arg is not None:
            if type_arg == type(source_code):
                if operation not in res_dict.keys():
                    res_dict[operation] = 1
                else:
                    res_dict[operation] = res_dict[operation] + 1
                res_mid: dict[str, int] = count_operations(e.argval)
                for key in res_mid.keys():
                    if key not in res_dict.keys():
                        res_dict[key] = res_mid[key]
                    else:
                        res_dict[key] = res_dict[key] + res_mid[key]
            else:
                if operation not in res_dict.keys():
                    res_dict[operation] = 1
                    continue
                res_dict[operation] = res_dict[operation] + 1
    return res_dict
