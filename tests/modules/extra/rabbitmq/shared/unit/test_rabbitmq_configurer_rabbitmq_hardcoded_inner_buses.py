from time import sleep
from typing import List, Type

import pytest
from meiga import BoolResult, isSuccess

from petisco import AllMessageSubscriber, Container, DomainEvent, DomainEventSubscriber
from petisco.extra.rabbitmq import RabbitMqConfigurer, get_rabbitmq_message_dependencies
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_domain_event_bus_mother import (
    RabbitMqDomainEventBusMother,
)
from tests.modules.extra.rabbitmq.utils.spy_messages import SpyMessages
from tests.modules.extra.testing_decorators import testing_with_rabbitmq


@pytest.mark.unit
class TestRabbitMqConfigurerRabbitMqHardcodedInnerBuses:
    store_alias: str
    derived_alias: str
    inner_organization: str
    inner_service: str

    def setup_method(self):
        self.store_alias = "main"
        self.derived_alias = "derived"
        self.inner_organization = "inner_organization"
        self.inner_service = "inner_service"

        dependencies = get_rabbitmq_message_dependencies(
            organization=DEFAULT_ORGANIZATION,
            service=DEFAULT_SERVICE,
            alias=self.store_alias,
        )
        inner_dependencies = get_rabbitmq_message_dependencies(
            organization=self.inner_organization,
            service=self.inner_service,
            alias=self.derived_alias,
        )
        Container.set_dependencies(dependencies + inner_dependencies)

    def teardown_method(self):
        Container.clear()

    @testing_with_rabbitmq
    def should_execute_configuring_rabbitmq_hardcoded_inner_bus(self):
        spy_store_consumer = SpyMessages()
        spy_derived_bus_handler = SpyMessages()

        class MainEvent(DomainEvent): ...

        class DerivedEvent(DomainEvent): ...

        main_event = MainEvent()
        derived_event = DerivedEvent()

        class StoreSubscriber(AllMessageSubscriber):
            def handle(self, domain_event: DomainEvent) -> BoolResult:
                self.domain_event_bus.publish(derived_event)
                spy_store_consumer.append(domain_event)
                return isSuccess

        class DerivedSubscriber(DomainEventSubscriber):
            def subscribed_to(self) -> List[Type[DomainEvent]]:
                return [DerivedEvent]

            def handle(self, domain_event: DomainEvent) -> BoolResult:
                spy_derived_bus_handler.append(domain_event)
                return isSuccess

        # Add configuration to force exchange creation i
        inner_configurer = RabbitMqConfigurer(
            subscribers=[DerivedSubscriber],
            inner_bus_organization=self.inner_organization,
            inner_bus_service=self.inner_service,
            alias=self.derived_alias,
            clear_subscriber_before=True,
            clear_store_before=True,
            use_container_buses=False,
        )
        inner_configurer.execute()

        main_configurer = RabbitMqConfigurer(
            subscribers=[StoreSubscriber],
            start_consuming=True,
            inner_bus_organization=self.inner_organization,
            inner_bus_service=self.inner_service,
            alias=self.store_alias,
            clear_store_before=True,
            use_container_buses=False,
        )
        main_configurer.execute()

        bus = RabbitMqDomainEventBusMother.default()
        bus.publish(main_event)

        sleep(2.0)

        main_configurer.stop()
        inner_configurer.stop()

        spy_store_consumer.assert_first_message(main_event)
        spy_derived_bus_handler.assert_first_message(derived_event)
