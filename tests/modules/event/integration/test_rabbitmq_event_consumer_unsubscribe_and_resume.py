from time import sleep

import pytest
from meiga import isSuccess, BoolResult, isFailure

from petisco import Event

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
def test_should_publish_consume_from_store_queue_from_rabbitmq_with_stop_and_start():

    spy = SpyEvents()

    def assert_consumer_event_store(event: Event) -> BoolResult:
        spy.append(event)
        return isSuccess

    bus = RabbitMqEventBusMother.default()

    first_event = EventUserCreatedMother.random()
    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_event(first_event)

    # First Start & Stop
    bus.publish(first_event)
    first_consumer = RabbitMqEventConsumerMother.default()
    first_consumer.add_handler_on_store(assert_consumer_event_store)
    first_consumer.start()
    sleep(1.0)
    first_consumer.stop()

    # Second Start & Stop
    second_event = EventUserCreatedMother.random()
    second_consumer = RabbitMqEventConsumerMother.default()
    second_consumer.add_handler_on_store(assert_consumer_event_store)
    second_consumer.start()
    bus.publish(second_event)
    sleep(1.0)
    second_consumer.stop()

    configurer.clear()

    spy.assert_number_unique_events(2)
    spy.assert_count_by_event_id(first_event.event_id, 1)
    spy.assert_count_by_event_id(second_event.event_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_unsubscribe_and_resume_handler_on_store_queue():

    spy = SpyEvents()
    spy_dead_letter = SpyEvents()

    def assert_consumer_event_store(event: Event) -> BoolResult:
        spy.append(event)
        return isSuccess

    def assert_consumer_event_dead_letter(event: Event) -> BoolResult:
        spy_dead_letter.append(event)
        return isSuccess

    bus = RabbitMqEventBusMother.default()

    first_event = EventUserCreatedMother.random()
    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_event(first_event)

    # Consumer configuration
    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_handler_on_store(assert_consumer_event_store)
    consumer.add_handler_on_queue(
        "dead_letter.store", assert_consumer_event_dead_letter
    )
    consumer.start()
    bus.publish(first_event)
    sleep(1.0)
    consumer.unsubscribe_handler_on_queue("store")

    for i in range(10):
        bus.publish(EventUserCreatedMother.random())
    sleep(5.0)

    consumer.resume_handler_on_queue("store")
    second_event = EventUserCreatedMother.random()
    bus.publish(second_event)
    sleep(3.0)
    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(2)
    spy.assert_count_by_event_id(first_event.event_id, 1)
    spy.assert_count_by_event_id(second_event.event_id, 1)

    spy_dead_letter.assert_number_unique_events(10)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_unsubscribe_and_resume_handler_on_dead_letter_store_queue():

    spy_dead_letter = SpyEvents()

    def assert_consumer_event_store(event: Event) -> BoolResult:
        return isFailure

    def assert_consumer_event_dead_letter(event: Event) -> BoolResult:
        spy_dead_letter.append(event)
        return isSuccess

    bus = RabbitMqEventBusMother.default()

    first_event = EventUserCreatedMother.random()
    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_event(first_event)

    # Consumer configuration
    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_handler_on_store(assert_consumer_event_store)
    consumer.add_handler_on_queue(
        "dead_letter.store", assert_consumer_event_dead_letter
    )
    consumer.start()

    for i in range(10):
        bus.publish(EventUserCreatedMother.random())
    sleep(5.0)

    consumer.unsubscribe_handler_on_queue("dead_letter.store")

    for i in range(10):
        bus.publish(EventUserCreatedMother.random())
    sleep(5.0)

    consumer.resume_handler_on_queue("dead_letter.store")

    for i in range(10):
        bus.publish(EventUserCreatedMother.random())
    sleep(5.0)

    consumer.stop()
    configurer.clear()

    spy_dead_letter.assert_number_unique_events(30)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_raise_an_error_when_unsubscribe_an_nonexistent_queue():
    def assert_consumer_event_store(event: Event) -> BoolResult:
        return isSuccess

    event = EventUserCreatedMother.random()
    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_event(event)

    # Consumer configuration
    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_handler_on_store(assert_consumer_event_store)
    consumer.start()

    with pytest.raises(IndexError) as excinfo:
        consumer.unsubscribe_handler_on_queue("nonexistent_queue")
        assert (
            "Cannot unsubscribe an nonexistent queue (nonexistent_queue). Please, check configured consumers"
            in str(excinfo.value)
        )

    consumer.stop()
    configurer.clear()


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_raise_an_error_when_resume_an_nonexistent_queue():
    def assert_consumer_event_store(event: Event) -> BoolResult:
        return isSuccess

    event = EventUserCreatedMother.random()
    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_event(event)

    # Consumer configuration
    consumer = RabbitMqEventConsumerMother.default()
    consumer.add_handler_on_store(assert_consumer_event_store)
    consumer.start()

    with pytest.raises(IndexError) as excinfo:
        consumer.resume_handler_on_queue("nonexistent_queue")
        assert (
            "Cannot resume an nonexistent queue (nonexistent_queue). Please, check configured consumers"
            in str(excinfo.value)
        )
    consumer.stop()
    configurer.clear()
