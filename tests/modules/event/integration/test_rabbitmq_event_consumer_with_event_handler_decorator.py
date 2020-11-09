from time import sleep

import pytest
from meiga import isFailure, Result, Error, isSuccess, Failure

from petisco import Event, event_handler, DEBUG
from petisco.domain.errors.critical_error import CriticalError
from petisco.event.shared.domain.event_subscriber import EventSubscriber

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
from tests.modules.unit.mocks.fake_logger import FakeLogger
from tests.modules.unit.mocks.fake_notifier import FakeNotifier
from tests.modules.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_with_event_handler_when_success_consumer():
    spy = SpyEvents()
    logger = FakeLogger()

    @event_handler(logger=logger)
    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.without_retry()
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    first_logging_message = logger.get_logging_messages()[0]
    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_event_handler(
            operation="assert_consumer",
            message={"event": event.event_name, "body": event.to_json()},
        ).to_dict(),
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_with_event_handler_with_default_parameters_when_success_consumer(
    given_any_petisco
):
    spy = SpyEvents()

    @event_handler()
    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.without_retry()
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_with_event_handler_when_fail_consumer_without_retry():
    spy = SpyEvents()
    logger = FakeLogger()

    @event_handler(logger=logger)
    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isFailure

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.without_retry()
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    first_logging_message = logger.get_logging_messages()[0]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_event_handler(
            operation="assert_consumer",
            message={"event": event.event_name, "body": event.to_json()},
        ).to_dict(),
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_with_event_handler_when_fail_consumer():
    spy = SpyEvents()
    logger = FakeLogger()

    @event_handler(logger=logger)
    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isFailure

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(1)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    first_logging_message = logger.get_logging_messages()[0]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_event_handler(
            operation="assert_consumer",
            message={"event": event.event_name, "body": event.to_json()},
        ).to_dict(),
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_with_event_handler_return_nothing():
    spy = SpyEvents()
    logger = FakeLogger()

    @event_handler(logger=logger)
    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_max_retries(5)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)  # If returns isFailure it would retry
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    first_logging_message = logger.get_logging_messages()[0]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_event_handler(
            operation="assert_consumer",
            message={"event": event.event_name, "body": event.to_json()},
        ).to_dict(),
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_with_event_handler_notify_when_fail_consumer_with_critical_error(
    given_any_petisco
):
    spy = SpyEvents()
    logger = FakeLogger()
    notifier = FakeNotifier()

    class MyCriticalError(CriticalError):
        pass

    @event_handler(logger=logger, notifier=notifier)
    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return Failure(MyCriticalError(Exception()))

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.without_retry()
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    first_logging_message = logger.get_logging_messages()[0]
    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_event_handler(
            operation="assert_consumer",
            message={"event": event.event_name, "body": event.to_json()},
        ).to_dict(),
    )
    assert notifier.publish_called
    assert notifier.publish_times_called == 1


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_consume_with_event_handler_not_notify_when_fail_consumer_with_critical_error():
    spy = SpyEvents()
    logger = FakeLogger()
    notifier = FakeNotifier()

    @event_handler(logger=logger, notifier=notifier)
    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        raise Exception()

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.default()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.without_retry()
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    first_logging_message = logger.get_logging_messages()[0]
    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_event_handler(
            operation="assert_consumer",
            message={"event": event.event_name, "body": event.to_json()},
        ).to_dict(),
    )
    assert not notifier.publish_called
