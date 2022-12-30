from copy import deepcopy
from typing import Dict, Any

def map_dictionary(to_be_mapped: Dict[str, Any], key_map: Dict[str, str], reverse: bool = False) -> Dict[str, Any]:
    mapped_dict = deepcopy(to_be_mapped)

    for key, val in key_map.items():
        if reverse:
            mapped_dict[key] = mapped_dict.pop(val)
        else:
            mapped_dict[val] = mapped_dict.pop(key)

    return mapped_dict

def build_insert_stmts(mapped_dict: Dict[str, Any]) -> tuple:
    add_fields = mapped_dict.keys()
    values = {k: v for k, v in mapped_dict.items() if k in add_fields}
    fields_stmt = ', '.join(add_fields)
    values_stmt = ', '.join(f':{add_field}' for add_field in add_fields)
    return fields_stmt, values_stmt

def build_update_stmt(mapped_dict: Dict[str, Any]) -> str:
    update_fields = mapped_dict.keys()
    update_stmt = ', '.join(f'{update_field} = :{update_field}' for update_field in update_fields)
    return update_stmt
