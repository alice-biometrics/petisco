from typing import Callable, Dict

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


def get_param(kdict: Dict, key: str):
    value = kdict.get(key)
    if not value:
        raise TypeError(f"ConfigEventSubscriber: {key} is a required parameter")
    return value


@dataclass
class ConfigEventSubscriber:
    organization: str
    service: str
    topic: str
    dead_letter: bool = False
    handler_key: str = None
    handler: Callable = None
    kdict: Dict = None

    def __repr__(self):
        return f"EventSubscriberConfig: {self.organization} | {self.service} | {self.topic} | {self.dead_letter} -> {self.handler}"

    @staticmethod
    def from_dict(kdict: Dict):
        organization = get_param(kdict, "organization")
        service = get_param(kdict, "service")
        handler_key = get_param(kdict, "handler")
        topic = get_param(kdict, "topic")
        dead_letter = kdict.get("dead_letter", False)

        return ConfigEventSubscriber(
            organization=organization,
            service=service,
            handler_key=handler_key,
            topic=topic,
            dead_letter=dead_letter,
            kdict=kdict,
        )

    def get_handler(self):
        # Use this function to avoid circular dependency accessing Petisco objects before its configuration

        if self.handler_key:
            handler = (
                get_function_from_string(self.handler_key)
                .handle(
                    on_failure=raise_petisco_config_exception,
                    failure_args=(self.kdict, "events:subscriber:subscriber"),
                )
                .unwrap()
            )
        else:
            handler = self.handler

        return handler
