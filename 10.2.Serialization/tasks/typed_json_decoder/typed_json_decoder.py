import typing as tp
import json

from decimal import Decimal

<<<<<<< HEAD

def change_type_recursively(obj_change: dict[tp.Any, tp.Any] | list[tp.Any]) -> dict[tp.Any, tp.Any] | list[tp.Any]:
    if isinstance(obj_change, dict):
        dct_res: dict[tp.Any, tp.Any] = dict()
        for key in obj_change.keys():
            if isinstance(obj_change[key], dict) and "__custom_key_type__" in obj_change[key].keys():
                new_dict_changed: dict[tp.Any, tp.Any] | list[tp.Any] = change_type_recursively(obj_change[key])
                dct_res[key] = new_dict_changed
            else:
                dct_res[key] = obj_change[key]
        if "__custom_key_type__" in dct_res.keys():
            type_change: str = dct_res["__custom_key_type__"]
            del dct_res["__custom_key_type__"]
            del obj_change["__custom_key_type__"]
            types_mapping: dict[str, type] = dict()
            types_mapping['int'] = int
            types_mapping['float'] = float
            types_mapping['decimal'] = Decimal
            for key in obj_change.keys():
                dct_res[types_mapping[type_change](key)] = obj_change[key]
                del dct_res[key]
            return dct_res
        return dct_res
    else:
        lst_res: list[tp.Any] = list()
        for el in obj_change:
            if isinstance(el, dict):
                new_dict: dict[tp.Any, tp.Any] | list[tp.Any] = change_type_recursively(el)
                lst_res.append(new_dict)
            else:
                lst_res.append(el)
        return lst_res


=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
<<<<<<< HEAD
    """
    deserialized_data: dict[tp.Any, tp.Any] | list[tp.Any] = json.loads(json_value)
    return change_type_recursively(deserialized_data)
=======
    """
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
