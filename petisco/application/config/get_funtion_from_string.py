import importlib
from typing import Callable


def get_function_from_string(function_string: str) -> Callable:
    if not function_string:
        return None
    mod_name, func_name = function_string.rsplit(".", 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    return func
