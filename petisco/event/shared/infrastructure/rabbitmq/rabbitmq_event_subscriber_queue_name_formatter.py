import re

from petisco.event.shared.domain.event_subscriber import EventSubscriber


class RabbitMqEventSubscriberQueueNameFormatter:
    @staticmethod
    def format(subscriber: EventSubscriber, exchange_name: str = None) -> str:
        event_name = (
            re.sub(r"(?<!^)(?=[A-Z])", "_", subscriber.event_name)
            .lower()
            .replace(".", "_")
        )
        event_name = f"{subscriber.event_version}.event.{event_name}"
        return f"{exchange_name}.{event_name}" if exchange_name else event_name

    @staticmethod
    def format_retry(subscriber: EventSubscriber, exchange_name: str = None) -> str:
        queue_name = RabbitMqEventSubscriberQueueNameFormatter.format(
            subscriber, exchange_name
        )
        return f"retry.{queue_name}"

    @staticmethod
    def format_dead_letter(
        subscriber: EventSubscriber, exchange_name: str = None
    ) -> str:
        queue_name = RabbitMqEventSubscriberQueueNameFormatter.format(
            subscriber, exchange_name
        )
        return f"dead_letter.{queue_name}"
