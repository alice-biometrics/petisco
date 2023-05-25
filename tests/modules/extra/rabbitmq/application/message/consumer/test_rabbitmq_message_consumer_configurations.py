from time import sleep

import pytest
from meiga import BoolResult, isFailure, isSuccess

from petisco import DomainEvent, DomainEventBus
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.rabbitmq.mother.message_subscriber_mother import (
    MessageSubscriberMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_domain_event_bus_mother import (
    RabbitMqDomainEventBusMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_message_configurer_mother import (
    RabbitMqMessageConfigurerMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_message_consumer_mother import (
    RabbitMqMessageConsumerMother,
)
from tests.modules.extra.rabbitmq.utils.spy_messages import SpyMessages
from tests.modules.extra.testing_decorators import testing_with_rabbitmq


@pytest.mark.integration
class TestRabbitMqMessageConsumerConfigurations:
    @testing_with_rabbitmq
    def should_configure_two_services_without_subscribers(self):
        spy = SpyMessages()

        def assert_store(domain_event: DomainEvent) -> BoolResult:
            spy.append(domain_event)
            return isSuccess

        configurer_service_1 = RabbitMqMessageConfigurerMother.with_service("service1")
        configurer_service_1.configure()

        configurer_service_2 = RabbitMqMessageConfigurerMother.with_service("service2")
        configurer_service_2.configure()

        domain_event = DomainEventUserCreatedMother.random()
        bus = RabbitMqDomainEventBusMother.with_service("service1")
        bus.publish(domain_event)

        consumer = RabbitMqMessageConsumerMother.default()
        consumer.add_subscribers(
            [MessageSubscriberMother.all_messages_subscriber(handler=assert_store)]
        )
        consumer.start()

        sleep(1.0)

        consumer.stop()
        configurer_service_1.clear()
        configurer_service_2.clear()

        spy.assert_number_unique_messages(1)
        spy.assert_first_message(domain_event)
        spy.assert_last_message(domain_event)
        spy.assert_count_by_message_id(domain_event.get_message_id(), 1)

    @testing_with_rabbitmq
    @pytest.mark.parametrize(
        "publish_events_service_1, publish_events_service_2, expected_unique_events, expected_total_received_events, simulated_results_store",
        [
            (
                1,
                0,
                1,
                6,
                [isFailure, isFailure, isFailure, isFailure, isFailure, isSuccess],
            ),
            (100, 0, 100, 100, 100 * [isSuccess]),
            (1, 0, 1, 2, [isFailure, isSuccess]),
            (1, 0, 1, 3, [isFailure, isFailure, isSuccess]),
            (1, 1, 2, 2, [isSuccess, isSuccess]),
            (5, 10, 15, 15, 15 * [isSuccess]),
            (5, 5, 10, 20, 50 * [isFailure, isSuccess]),
        ],
    )
    def should_configure_two_services_without_subscribers_and_consuming_event_from_store_queues(
        self,
        publish_events_service_1,
        publish_events_service_2,
        expected_unique_events,
        expected_total_received_events,
        simulated_results_store,
    ):
        spy = SpyMessages()

        def assert_store(domain_event: DomainEvent) -> BoolResult:
            spy.append(domain_event)
            result = simulated_results_store.pop(0)
            return result

        configurer_service_1 = RabbitMqMessageConfigurerMother.with_service("service1")
        configurer_service_1.configure()

        configurer_service_2 = RabbitMqMessageConfigurerMother.with_service("service2")
        configurer_service_2.configure()

        bus_service_1 = RabbitMqDomainEventBusMother.with_service("service1")
        bus_service_2 = RabbitMqDomainEventBusMother.with_service("service2")

        def publish_event(bus: DomainEventBus, times: int):
            for _ in range(times):
                event = DomainEventUserCreatedMother.random()
                bus.publish(event)

        publish_event(bus_service_1, publish_events_service_1)
        publish_event(bus_service_2, publish_events_service_2)

        consumer = RabbitMqMessageConsumerMother.with_service("service1")
        consumer.add_subscribers(
            [MessageSubscriberMother.all_messages_subscriber(handler=assert_store)]
        )
        consumer.start()

        sleep(1.0)

        consumer.stop()
        configurer_service_1.clear()
        configurer_service_2.clear()

        spy.assert_number_unique_messages(expected_unique_events)
        spy.assert_number_total_messages(expected_total_received_events)
