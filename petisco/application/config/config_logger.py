from typing import Optional

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


@dataclass
class ConfigLogger:
    selected_logger: Optional[str] = "not_implemented_logger"
    name: Optional[str] = None
    format: Optional[str] = None
    config: Optional[str] = None

    @staticmethod
    def from_dict(kdict):
        config = (
            get_function_from_string(kdict.get("config"))
            .handle(on_failure=raise_petisco_config_exception, failure_args=kdict)
            .unwrap()
        )

        return ConfigLogger(
            selected_logger=kdict.get("selected_logger", "not_implemented_logger"),
            name=kdict.get("name"),
            format=kdict.get("format", "%(name)s - %(levelname)s - %(message)s"),
            config=config,
        )
