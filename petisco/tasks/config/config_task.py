from typing import Callable, Dict

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


def get_float_if_exist(kdict: Dict, value: str) -> float:
    value = kdict.get(value)
    if value:
        value = float(value)
    return value


@dataclass
class ConfigTask:
    handler_key: str
    run_in: float = None
    cron_interval: float = None
    kdict: Dict = None

    @staticmethod
    def from_dict(kdict):
        run_in = get_float_if_exist(kdict, "run_in")
        cron_interval = get_float_if_exist(kdict, "cron_interval")
        handler_key = kdict.get("handler")

        if not handler_key:
            raise TypeError(f"ConfigTask: handler is a required parameter")

        return ConfigTask(
            run_in=run_in,
            handler_key=handler_key,
            cron_interval=cron_interval,
            kdict=kdict,
        )

    def get_handler(self) -> Callable:
        # Use this function to avoid circular dependency accessing Petisco objects before its configuration
        handler = (
            get_function_from_string(self.handler_key)
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(self.kdict, "tasks:*:handler"),
            )
            .unwrap()
        )
        return handler
