from typing import Dict

from petisco.legacy.event.legacy.publisher.domain.interface_event_publisher import (
    IEventPublisher,
)
from petisco.legacy.event.legacy.publisher.infrastructure.not_implemented_event_publisher import (
    NotImplementedEventPublisher,
)
from petisco.legacy.event.legacy.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.legacy.event.legacy.subscriber.domain.interface_event_subscriber import (
    IEventSubscriber,
)
from petisco.legacy.event.legacy.subscriber.infrastructure.not_implemented_event_subscriber import (
    NotImplementedEventSubscriber,
)


def event_publisher_provider() -> IEventPublisher:
    return NotImplementedEventPublisher()


def event_subscriber_provider(
    subscribers: Dict[str, ConfigEventSubscriber]
) -> IEventSubscriber:
    return NotImplementedEventSubscriber(subscribers)
