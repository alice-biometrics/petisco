import re

from petisco.base.domain.message.message_subscriber import MessageSubscriber


class RabbitMqMessageSubscriberQueueNameFormatter:
    @staticmethod
    def format(subscriber: MessageSubscriber, exchange_name: str = None) -> str:
        message_name = (
            re.sub(r"(?<!^)(?=[A-Z])", "_", subscriber.message_name)
            .lower()
            .replace(".", "_")
        )
        message_type = (
            subscriber.message_type
            if subscriber.message_type != "domain_event"
            else "event"
        )
        message_format = f"{subscriber.message_version}.{message_type}.{message_name}"
        return f"{exchange_name}.{message_format}" if exchange_name else message_format

    @staticmethod
    def format_retry(subscriber: MessageSubscriber, exchange_name: str = None) -> str:
        queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format(
            subscriber, exchange_name
        )
        return f"retry.{queue_name}"

    @staticmethod
    def format_dead_letter(
        subscriber: MessageSubscriber, exchange_name: str = None
    ) -> str:
        queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format(
            subscriber, exchange_name
        )
        return f"dead_letter.{queue_name}"
