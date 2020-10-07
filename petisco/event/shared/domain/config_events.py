import os
import re
import traceback
from typing import Optional, List, Any, Callable, Dict

import yaml
from dataclasses import dataclass
from meiga import Result, Error, Failure, Success
from meiga.decorators import meiga

from petisco.application.config.check_list_or_str_item import check_list_or_str_item
from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)
from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.application.config.config_file_not_found_error import (
    ConfigFileNotFoundError,
)
from yaml.parser import ParserError, ScannerError

from petisco.application.config.config_file_not_valid_error import (
    ConfigFileNotValidError,
)


def get_event_name(src_event_name: str) -> str:
    event_name = (
        re.sub(r"(?<!^)(?=[A-Z])", "_", src_event_name).lower().replace(".", "_")
    )
    return event_name


def get_handlers(handlers_names: List[str], kdict: Dict) -> List[Callable]:
    handlers = []
    for handler_name in handlers_names:
        handler = (
            get_function_from_string(handler_name)
            .handle(on_failure=raise_petisco_config_exception, failure_args=kdict)
            .unwrap()
        )
        handlers.append(handler)
    return handlers


@dataclass
class ConfigEvents:
    organization: str
    service: str
    consumer_verbose: bool = False
    use_store_queues: bool = True
    retry_ttl: int = 5000
    max_retries: int = 5
    message_broker: Optional[str] = "not_implemented"
    event_subscribers: Optional[List[EventSubscriber]] = None

    def __post_init__(self):
        message_broker = os.environ.get("PETISCO_EVENT_MESSAGE_BROKER")
        if message_broker:
            self.message_broker = message_broker

    @staticmethod
    @meiga
    def from_filename(filename: str) -> Result[Any, Error]:
        if not os.path.isfile(filename):
            return Failure(ConfigFileNotFoundError(filename))
        try:
            with open(filename) as file:
                petisco_dict = yaml.load(file, Loader=yaml.FullLoader)
                config_event = ConfigEvents.from_dict(petisco_dict)
                return Success(config_event)
        except (ParserError, ScannerError) as e:
            message = f"Error loading {filename} file: {repr(e.__class__)} {e} | {traceback.format_exc()}"
            return Failure(ConfigFileNotValidError(message))

    @staticmethod
    def from_dict(kdict):
        event_subscribers = None
        events = kdict.get("events")

        subscribers = events.get("subscribers")
        if subscribers:
            event_subscribers = []
            for src_event_name, event_info in subscribers.items():
                handlers_names = check_list_or_str_item(
                    event_info, "handlers", typename="EventHandler"
                )

                event_name = get_event_name(src_event_name)
                event_version = event_info.get("version", 1)
                handlers = get_handlers(handlers_names, kdict)

                event_subscribers.append(
                    EventSubscriber(
                        event_name=event_name,
                        event_version=event_version,
                        handlers=handlers,
                    )
                )

        return ConfigEvents(
            organization=events.get("organization"),
            service=events.get("service"),
            consumer_verbose=events.get("consumer_verbose", False),
            use_store_queues=events.get("use_store_queues", True),
            retry_ttl=events.get("retry_ttl", 5000),
            max_retries=events.get("max_retries", 5),
            message_broker=events.get("message_broker", "not_implemented"),
            event_subscribers=event_subscribers,
        )
