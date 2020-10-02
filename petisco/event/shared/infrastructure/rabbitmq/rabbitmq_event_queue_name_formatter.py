from petisco.event.shared.domain.event import Event


class RabbitMqEventQueueNameFormatter:
    @staticmethod
    def format(event: Event, exchange_name: str = None) -> str:
        event_name = event.event_name.replace(".", "_")
        event_name = f"{event.event_version}.event.{event_name}"
        return f"{exchange_name}.{event_name}" if exchange_name else event_name

    @staticmethod
    def format_retry(event: Event, exchange_name: str = None) -> str:
        queue_name = RabbitMqEventQueueNameFormatter.format(event, exchange_name)
        return f"retry.{queue_name}"

    @staticmethod
    def format_dead_letter(event: Event, exchange_name: str = None) -> str:
        queue_name = RabbitMqEventQueueNameFormatter.format(event, exchange_name)
        return f"dead_letter.{queue_name}"
