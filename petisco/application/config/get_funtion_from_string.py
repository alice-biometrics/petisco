import sys
import importlib
import traceback
from typing import Callable

from meiga import Result, Error, Success, isFailure


def get_function_from_string(function_string: str) -> Result[Callable, Error]:
    if not function_string:
        return Success(None)
    try:
        mod_name, func_name = function_string.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        return Success(func)
    except Exception as err:
        traceback.print_exc()
        print(err, file=sys.stderr)
        return isFailure
