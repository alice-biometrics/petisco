from typing import Optional

from dataclasses import dataclass

from petisco.application.config.events.config_event_publisher import (
    ConfigEventsPublisher,
)
from petisco.application.config.events.config_event_subscriber import (
    ConfigEventsSubscriber,
)


@dataclass
class ConfigEvents:
    publish_deploy_event: Optional[bool] = False
    config_event_publisher: Optional[ConfigEventsPublisher] = ConfigEventsPublisher()
    config_event_subscriber: Optional[ConfigEventsSubscriber] = ConfigEventsSubscriber()

    @staticmethod
    def from_dict(kdict):
        if not kdict or not isinstance(kdict, dict):
            return ConfigEvents()

        config_event_publisher = ConfigEventsPublisher()
        config_event_publisher_dict = kdict.get("publisher")
        if config_event_publisher_dict:
            config_event_publisher = ConfigEventsPublisher.from_dict(
                config_event_publisher_dict
            )

        config_event_subscriber = ConfigEventsSubscriber()
        config_event_subscriber_dict = kdict.get("subscriber")
        if config_event_subscriber_dict:
            config_event_subscriber = ConfigEventsSubscriber.from_dict(
                config_event_subscriber_dict
            )

        return ConfigEvents(
            publish_deploy_event=kdict.get("publish_deploy_event"),
            config_event_publisher=config_event_publisher,
            config_event_subscriber=config_event_subscriber,
        )
