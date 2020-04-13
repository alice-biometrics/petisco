from typing import Callable

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from petisco.application.config.get_funtion_from_string import get_function_from_string


@dataclass_json
@dataclass
class ConfigLogger:
    selected_logger: str
    name: str
    format: str
    config_func: str

    def get_config_func(self) -> Callable:
        return get_function_from_string(self.config_func)
