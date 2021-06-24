from typing import Type, Callable, List

from meiga import BoolResult

from petisco import DomainEvent, DomainEventSubscriber, AllMessageSubscriber, Command


class MessageSubscriberMother:
    @staticmethod
    def domain_event_subscriber(
        domain_event_type: Type[DomainEvent], handler: Callable
    ):
        class MyDomainEventSubscriber(DomainEventSubscriber):
            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [domain_event_type]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return handler(domain_event)

        return MyDomainEventSubscriber

    @staticmethod
    def all_messages_subscriber(handler: Callable):
        class MyDomainEventSubscriber(AllMessageSubscriber):
            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return handler(domain_event)

        return MyDomainEventSubscriber

    @staticmethod
    def command_subscriber(command_type: Type[Command], handler: Callable):
        class MyComandSubscriber(DomainEventSubscriber):
            def subscribed_to(self) -> List[Type[Command]]:
                return [command_type]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                return handler(domain_event)

        return MyComandSubscriber
