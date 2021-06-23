import re

from petisco.base.domain.message.message_subscriber_info import MessageSubscriberInfo


class RabbitMqMessageSubscriberQueueNameFormatter:
    @staticmethod
    def format(
        subscriber_info: MessageSubscriberInfo, exchange_name: str = None
    ) -> str:
        message_name = (
            re.sub(r"(?<!^)(?=[A-Z])", "_", subscriber_info.message_name)
            .lower()
            .replace(".", "_")
        )
        message_type = (
            subscriber_info.message_type
            if subscriber_info.message_type != "domain_event"
            else "event"
        )
        message_format = (
            f"{subscriber_info.message_version}.{message_type}.{message_name}"
        )
        return f"{exchange_name}.{message_format}" if exchange_name else message_format

    @staticmethod
    def format_retry(
        subscriber_info: MessageSubscriberInfo, exchange_name: str = None
    ) -> str:
        queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format(
            subscriber_info, exchange_name
        )
        return f"retry.{queue_name}"

    @staticmethod
    def format_dead_letter(
        subscriber_info: MessageSubscriberInfo, exchange_name: str = None
    ) -> str:
        queue_name = RabbitMqMessageSubscriberQueueNameFormatter.format(
            subscriber_info, exchange_name
        )
        return f"dead_letter.{queue_name}"
