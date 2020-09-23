from typing import Optional, Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)
from petisco.event.legacy.publisher.infrastructure.not_implemented_event_publisher import (
    NotImplementedEventPublisher,
)


@dataclass
class ConfigEventsPublisher:
    provider: Optional[Callable] = lambda: NotImplementedEventPublisher()

    @staticmethod
    def from_dict(kdict):

        provider = kdict.get("provider")
        if not provider:
            raise TypeError(
                f"ConfigEventsPublisher: {provider} is a required parameter"
            )

        provider = (
            get_function_from_string(provider)
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "event:publisher:provider"),
            )
            .unwrap()
        )

        return ConfigEventsPublisher(provider=provider)
