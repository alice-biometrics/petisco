from typing import Dict

from petisco.events.publisher.domain.interface_event_publisher import IEventPublisher
from petisco.events.publisher.infrastructure.not_implemented_event_publisher import (
    NotImplementedEventPublisher,
)
from petisco.events.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.events.subscriber.domain.interface_event_subscriber import IEventSubscriber
from petisco.events.subscriber.infrastructure.not_implemented_event_subscriber import (
    NotImplementedEventSubscriber,
)


def event_publisher_provider() -> IEventPublisher:
    return NotImplementedEventPublisher()


def event_subscriber_provider(
    subscribers: Dict[str, ConfigEventSubscriber]
) -> IEventSubscriber:
    return NotImplementedEventSubscriber(subscribers)
