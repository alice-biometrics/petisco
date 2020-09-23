from typing import Optional, Dict, Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)
from petisco.event.legacy.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.event.legacy.subscriber.infrastructure.not_implemented_event_subscriber import (
    NotImplementedEventSubscriber,
)


@dataclass
class ConfigEventsSubscriber:
    provider: Optional[Callable] = lambda subscribers: NotImplementedEventSubscriber(
        subscribers
    )
    subscribers: Optional[Dict[str, ConfigEventSubscriber]] = None

    @staticmethod
    def from_dict(kdict):

        provider = kdict.get("provider")
        if not provider:
            raise TypeError(
                f"ConfigEventsSubscriber: {provider} is a required parameter"
            )
        provider = (
            get_function_from_string(provider)
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "event:subscriber:provider"),
            )
            .unwrap()
        )

        subscribers = {}
        subscribers_dict = kdict.get("subscribers")
        if subscribers_dict:
            if not isinstance(subscribers_dict, dict):
                raise TypeError(
                    f"ConfigEventManager: subscribers must be a Dict with information about event subscribers"
                )
            subscribers = {
                k: ConfigEventSubscriber.from_dict(v)
                for k, v in subscribers_dict.items()
            }

        return ConfigEventsSubscriber(provider=provider, subscribers=subscribers)
