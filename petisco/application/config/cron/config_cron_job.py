from typing import Callable, Dict

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


@dataclass
class ConfigCronJob:
    seconds: float
    handler_key: str
    kdict: Dict = None

    @staticmethod
    def from_dict(kdict):
        seconds = kdict.get("seconds")
        handler_key = kdict.get("handler")
        if not handler_key:
            raise TypeError(f"ConfigEventsSubscriber: handler is a required parameter")

        return ConfigCronJob(seconds, handler_key, kdict)

    def get_handler(self) -> Callable:
        # Use this function to avoid circular dependency accessing Petisco objects before its configuration
        handler = (
            get_function_from_string(self.handler_key)
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(self.kdict, "cron:*:handler"),
            )
            .unwrap()
        )
        return handler
