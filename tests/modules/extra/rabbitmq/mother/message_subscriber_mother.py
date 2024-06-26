from typing import Callable, List, Type

from meiga import BoolResult

from petisco import (
    AllMessageSubscriber,
    Command,
    CommandSubscriber,
    DomainEvent,
    DomainEventSubscriber,
)


class MessageSubscriberMother:
    @staticmethod
    def domain_event_subscriber(domain_event_type: Type[DomainEvent], handler: Callable):
        class MyDomainEventSubscriber(DomainEventSubscriber):
            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [domain_event_type]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return handler(domain_event)

        return MyDomainEventSubscriber

    @staticmethod
    def domain_event_subscriber_with_self_handler(
        domain_event_type: Type[DomainEvent], self_handler: Callable
    ):
        class MyDomainEventSubscriber(DomainEventSubscriber):
            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [domain_event_type]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return self_handler(self, domain_event)

        return MyDomainEventSubscriber

    @staticmethod
    def other_domain_event_subscriber(domain_event_type: Type[DomainEvent], handler: Callable):
        class MyOtherDomainEventSubscriber(DomainEventSubscriber):
            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [domain_event_type]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return handler(domain_event)

        return MyOtherDomainEventSubscriber

    @staticmethod
    def all_messages_subscriber(handler: Callable):
        class MyAllMessageSubscriber(AllMessageSubscriber):
            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return handler(domain_event)

        return MyAllMessageSubscriber

    @staticmethod
    def other_all_messages_subscriber(handler: Callable):
        class MyOtherAllMessageSubscriber(AllMessageSubscriber):
            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return handler(domain_event)

        return MyOtherAllMessageSubscriber

    @staticmethod
    def command_subscriber(command_type: Type[Command], handler: Callable):
        class MyComandSubscriber(CommandSubscriber):
            def subscribed_to(self) -> Type[Command]:
                return command_type

            def handle(self, command: Command) -> BoolResult:
                return handler(command)

        return MyComandSubscriber
