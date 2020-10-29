from time import sleep

import pytest
from meiga import isSuccess, isFailure, BoolResult

from petisco import Event, IEventBus

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.modules.event.mothers.event_user_created_mother import EventUserCreatedMother
from tests.modules.event.mothers.rabbitmq_event_bus_mother import RabbitMqEventBusMother
from tests.modules.event.mothers.rabbitmq_event_configurer_mother import (
    RabbitMqEventConfigurerMother,
)
from tests.modules.event.mothers.rabbitmq_event_consumer_mother import (
    RabbitMqEventConsumerMother,
)
from tests.modules.event.spies.spy_events import SpyEvents


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_configure_two_services_without_subscribers():
    spy = SpyEvents()

    def assert_store(event: Event) -> BoolResult:
        spy.append(event)
        return isSuccess

    configurer_service_1 = RabbitMqEventConfigurerMother.with_service("service1")
    configurer_service_1.configure()

    configurer_service_2 = RabbitMqEventConfigurerMother.with_service("service2")
    configurer_service_2.configure()

    event = EventUserCreatedMother.random()
    bus = RabbitMqEventBusMother.with_service("service1")
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_handler_on_store(assert_store)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer_service_1.clear()
    configurer_service_2.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_last_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)


@pytest.mark.integration
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
def test_should_configure_two_services_without_subscribers_and_consuming_event_from_store_queues(
    publish_events_service_1,
    publish_events_service_2,
    expected_unique_events,
    expected_total_received_events,
    simulated_results_store,
):
    spy = SpyEvents()

    def assert_store(event: Event) -> BoolResult:
        spy.append(event)
        result = simulated_results_store.pop(0)
        return result

    configurer_service_1 = RabbitMqEventConfigurerMother.with_service("service1")
    configurer_service_1.configure()

    configurer_service_2 = RabbitMqEventConfigurerMother.with_service("service2")
    configurer_service_2.configure()

    bus_service_1 = RabbitMqEventBusMother.with_service("service1")
    bus_service_2 = RabbitMqEventBusMother.with_service("service2")

    def publish_event(bus: IEventBus, times: int):
        for _ in range(times):
            event = EventUserCreatedMother.random()
            bus.publish(event)

    publish_event(bus_service_1, publish_events_service_1)
    publish_event(bus_service_2, publish_events_service_2)

    consumer = RabbitMqEventConsumerMother.with_service("service1")
    consumer.add_handler_on_store(assert_store)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer_service_1.clear()
    configurer_service_2.clear()

    spy.assert_number_unique_events(expected_unique_events)
    spy.assert_number_total_events(expected_total_received_events)
