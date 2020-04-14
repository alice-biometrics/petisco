from typing import Callable, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from petisco.application.config.get_funtion_from_string import get_function_from_string


@dataclass_json
@dataclass
class ConfigLogger:
    selected_logger: Optional[str] = "not_implemented_logger"
    name: Optional[str] = None
    format: Optional[str] = None
    config_func: Optional[str] = None

    def get_config_func(self) -> Callable:
        return get_function_from_string(self.config_func)
