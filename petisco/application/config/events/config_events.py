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

        config_event_publisher = None
        config_event_publisher_dict = kdict.get("publisher")
        if config_event_publisher_dict:
            config_event_publisher = ConfigEventsPublisher.from_dict(
                config_event_publisher_dict
            )

        config_event_subscriber = None
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
