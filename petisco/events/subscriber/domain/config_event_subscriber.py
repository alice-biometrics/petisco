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
    handler: Callable
    topic: str
    dead_letter: bool = False

    def __repr__(self):
        return f"EventSubscriberConfig: {self.organization} | {self.service} | {self.topic} | {self.dead_letter} -> {self.handler}"

    @staticmethod
    def from_dict(kdict: Dict):
        organization = get_param(kdict, "organization")
        service = get_param(kdict, "service")
        topic = get_param(kdict, "topic")
        dead_letter = kdict.get("dead_letter", False)

        handler = (
            get_function_from_string(get_param(kdict, "handler"))
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "events:subscriber:subscriber"),
            )
            .unwrap()
        )

        return ConfigEventSubscriber(
            organization=organization,
            service=service,
            handler=handler,
            topic=topic,
            dead_letter=dead_letter,
        )
