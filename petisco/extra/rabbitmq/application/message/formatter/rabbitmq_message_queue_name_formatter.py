from petisco.base.domain.message.message import Message


class RabbitMqMessageQueueNameFormatter:
    @staticmethod
    def format(message: Message, exchange_name: str = None) -> str:
        message_name = message.name.replace(".", "_")
        message_type = message.type if message.type != "domain_event" else "event"
        message_format = f"{message.version}.{message_type}.{message_name}"
        return f"{exchange_name}.{message_format}" if exchange_name else message_name

    @staticmethod
    def format_retry(message: Message, exchange_name: str = None) -> str:
        queue_name = RabbitMqMessageQueueNameFormatter.format(message, exchange_name)
        return f"retry.{queue_name}"

    @staticmethod
    def format_dead_letter(message: Message, exchange_name: str = None) -> str:
        queue_name = RabbitMqMessageQueueNameFormatter.format(message, exchange_name)
        return f"dead_letter.{queue_name}"
