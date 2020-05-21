from typing import Optional, Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)
from petisco.notifier.infrastructure.not_implemented_notifier import (
    NotImplementedNotifier,
)


def get_default_notifier():
    return NotImplementedNotifier()


@dataclass
class ConfigNotifier:
    provider: Optional[Callable] = None

    @staticmethod
    def from_dict(kdict):
        provider = get_default_notifier
        if kdict and isinstance(kdict, dict):
            provider = (
                get_function_from_string(kdict.get("provider"))
                .handle(
                    on_failure=raise_petisco_config_exception,
                    failure_args=(kdict, "notifier:provider"),
                )
                .unwrap()
            )

        return ConfigNotifier(provider=provider)
