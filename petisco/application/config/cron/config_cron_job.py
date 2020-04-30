from typing import Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


@dataclass
class ConfigCronJob:
    seconds: float
    handler: Callable

    @staticmethod
    def from_dict(kdict):
        seconds = kdict.get("seconds")
        handler = kdict.get("handler")
        if not handler:
            raise TypeError(
                f"ConfigEventsSubscriber: {handler} is a required parameter"
            )
        handler = (
            get_function_from_string(handler)
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "cron:*:handler"),
            )
            .unwrap()
        )

        return ConfigCronJob(seconds, handler)
