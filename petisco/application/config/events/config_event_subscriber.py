from typing import Optional, Dict, Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.events.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.events.subscriber.infrastructure.not_implemented_event_subscriber import (
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
        provider = get_function_from_string(provider)

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
