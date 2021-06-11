from petisco.base.domain.message.domain_event import DomainEvent


class RabbitMqDomainEventQueueNameFormatter:
    @staticmethod
    def format(domain_event: DomainEvent, exchange_name: str = None) -> str:
        event_name = domain_event.name.replace(".", "_")
        event_name = f"{domain_event.version}.event.{event_name}"
        return f"{exchange_name}.{event_name}" if exchange_name else event_name

    @staticmethod
    def format_retry(domain_event: DomainEvent, exchange_name: str = None) -> str:
        queue_name = RabbitMqDomainEventQueueNameFormatter.format(
            domain_event, exchange_name
        )
        return f"retry.{queue_name}"

    @staticmethod
    def format_dead_letter(domain_event: DomainEvent, exchange_name: str = None) -> str:
        queue_name = RabbitMqDomainEventQueueNameFormatter.format(
            domain_event, exchange_name
        )
        return f"dead_letter.{queue_name}"
