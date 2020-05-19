from typing import Callable, Dict

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


def get_float_if_exist(kdict: Dict, value: str, default_value=None) -> float:
    value = kdict.get(value)
    if value:
        value = float(value)
    else:
        value = default_value
    return value


def get_type(run_in, interval) -> str:
    if interval:
        type_task = "recurring"
    else:
        if run_in:
            type_task = "scheduled"
        else:
            type_task = "instant"
    return type_task


@dataclass
class ConfigTask:
    handler_key: str
    run_in: float = 0.0
    interval: float = None
    type: str = "instant"
    kdict: Dict = None

    def to_dict(self):
        kdict = {"type": self.type}
        if self.run_in is not None:
            kdict["run_in"] = self.run_in
        if self.interval is not None:
            kdict["interval"] = self.interval
        return kdict

    @staticmethod
    def from_dict(kdict):
        run_in = get_float_if_exist(kdict, "run_in", default_value=0.0)
        interval = get_float_if_exist(kdict, "interval")
        handler_key = kdict.get("handler")
        type = get_type(run_in, interval)

        if not handler_key:
            raise TypeError(f"ConfigTask: handler is a required parameter")

        return ConfigTask(
            run_in=run_in,
            handler_key=handler_key,
            interval=interval,
            type=type,
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
