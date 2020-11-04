from time import sleep

import pytest
from meiga import isSuccess, Result, Error, Failure

from petisco import Event, DEBUG
from petisco.event.chaos.domain.event_chaos_error import EventChaosError
from petisco.event.chaos.infrastructure.rabbitmq_event_chaos import RabbitMqEventChaos
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


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_consumer_react_to_default_no_chaos():

    spy = SpyEvents()
    logger = FakeLogger()

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

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    max_retries_allowed = 5
    chaos = RabbitMqEventChaos()
    consumer = RabbitMqEventConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    assert len(logger.get_logging_messages()) == 1
    logging_message = logger.get_logging_messages()[0]
    assert logging_message[0] == DEBUG
    assert logging_message[1]["data"]["message"]["derived_action"] == {}


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_consumer_react_to_chaos_with_zero_probability():

    spy = SpyEvents()
    logger = FakeLogger()

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

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    max_retries_allowed = 5
    chaos = RabbitMqEventChaos(
        percentage_simulate_nack=0.0, percentage_simulate_failures=0.0
    )
    consumer = RabbitMqEventConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_events(1)
    spy.assert_first_event(event)
    spy.assert_count_by_event_id(event.event_id, 1)

    assert len(logger.get_logging_messages()) == 1
    logging_message = logger.get_logging_messages()[0]
    assert logging_message[0] == DEBUG
    assert logging_message[1]["data"]["message"]["derived_action"] == {}


@pytest.mark.integration
@testing_with_rabbitmq
@pytest.mark.parametrize(
    "max_retries_allowed,expected_number_event_consumed,chaos",
    [
        (5, 0, RabbitMqEventChaos(percentage_simulate_nack=1.0)),
        (1, 2, RabbitMqEventChaos(percentage_simulate_failures=1.0)),
        (1, 1, RabbitMqEventChaos(delay_before_even_handler_second=2.0)),
    ],
)
def test_should_consumer_react_to_chaos_inputs(
    max_retries_allowed, expected_number_event_consumed, chaos
):
    spy = SpyEvents()

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

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    consumer = RabbitMqEventConsumerMother.with_chaos(chaos, max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()
    spy.assert_count_by_event_id(event.event_id, expected_number_event_consumed)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_consumer_react_to_chaos_with_nck_simulation_and_check_logger():

    spy = SpyEvents()
    logger = FakeLogger()

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

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    max_retries_allowed = 5
    chaos = RabbitMqEventChaos(percentage_simulate_nack=1.0)
    consumer = RabbitMqEventConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    assert len(logger.get_logging_messages()) >= 200
    first_logging_message = logger.get_logging_messages()[0]

    assert first_logging_message[0] == DEBUG
    assert first_logging_message[1]["meta"] == {
        "layer": "rabbitmq_event_consumer",
        "operation": "assert_consumer",
    }
    assert (
        first_logging_message[1]["data"]["message"]["chaos_action"] == "nck simulated"
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_consumer_react_to_chaos_with_failure_simulation_and_check_logger():

    spy = SpyEvents()
    logger = FakeLogger()

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

    configurer = RabbitMqEventConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    max_retries_allowed = 5
    chaos = RabbitMqEventChaos(percentage_simulate_failures=1.0)
    consumer = RabbitMqEventConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    assert_logger_represents_simulated_failure_scenario(logger, max_retries_allowed)


def assert_logger_represents_simulated_failure_scenario(logger, max_retries_allowed):
    assert len(logger.get_logging_messages()) == max_retries_allowed + 1
    for i in range(max_retries_allowed):
        redelivery_count = i + 1
        logging_message = logger.get_logging_messages()[i]

        assert logging_message[0] == DEBUG
        assert logging_message[1]["meta"] == {
            "layer": "rabbitmq_event_consumer",
            "operation": "assert_consumer",
        }
        assert logging_message[1]["data"]["message"]["result"] == Failure(
            EventChaosError(Exception())
        )

        derived_action = logging_message[1]["data"]["message"]["derived_action"]

        if i < 5:
            expected_derived_action = {
                "action": "send_to_retry",
                "exchange_name": "retry.alice.petisco",
                "routing_key": "retry.alice.petisco.1.event.user_created.assert_consumer",
                "headers": {
                    "queue": "alice.petisco.1.event.user_created.assert_consumer",
                    "redelivery_count": redelivery_count,
                },
            }
        else:
            expected_derived_action = {
                "action": "send_to_dead_letter",
                "exchange_name": "dead_letter.alice.petisco",
                "routing_key": "dead_letter.alice.petisco.1.event.user_created.assert_consumer",
                "headers": {
                    "queue": "alice.petisco.1.event.user_created.assert_consumer",
                    "redelivery_count": redelivery_count,
                },
            }

        if i > 0:
            derived_action["headers"].pop("x-death")
            derived_action["headers"].pop("x-first-death-exchange")
            derived_action["headers"].pop("x-first-death-queue")
            derived_action["headers"].pop("x-first-death-reason")

        assert derived_action == expected_derived_action


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_consumer_react_to_chaos_with_nck_simulation_and_send_event_to_dead_letter():
    spy = SpyEvents()
    spy_dead_letter = SpyEvents()
    spy_dead_letter_store = SpyEvents()
    logger = FakeLogger()

    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isSuccess

    def assert_dead_letter_consumer(event: Event) -> Result[bool, Error]:
        spy_dead_letter.append(event)
        return isSuccess

    def assert_dead_letter_store_consumer(event: Event) -> Result[bool, Error]:
        spy_dead_letter_store.append(event)
        return isSuccess

    event = EventUserCreatedMother.random()
    subscribers = [
        EventSubscriber(
            event_name=event.event_name,
            event_version=event.event_version,
            handlers=[assert_consumer],
        )
    ]

    configurer = RabbitMqEventConfigurerMother.with_main_and_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqEventBusMother.default()
    bus.publish(event)

    max_retries_allowed = 5
    chaos = RabbitMqEventChaos(percentage_simulate_nack=1.0)
    consumer_with_chaos = RabbitMqEventConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer_with_chaos.add_subscribers(subscribers)
    consumer_with_chaos.start()
    sleep(1.0)
    consumer_with_chaos.stop()

    consumer_without_chaos = RabbitMqEventConsumerMother.default()
    consumer_without_chaos.add_handler_on_queue(
        "dead_letter.alice.petisco.1.event.user_created.assert_consumer",
        assert_dead_letter_consumer,
    )
    consumer_without_chaos.add_handler_on_queue(
        "dead_letter.store", assert_dead_letter_store_consumer
    )

    consumer_without_chaos.start()
    sleep(1.0)
    consumer_without_chaos.stop()

    configurer.clear()

    spy.assert_count_by_event_id(event.event_id, 0)  # Rejected before by Event Chaos
    spy_dead_letter.assert_count_by_event_id(event.event_id, 1)
    spy_dead_letter_store.assert_count_by_event_id(event.event_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_store_consumer_react_to_chaos_with_nck_simulation_and_send_several_event_to_dead_letter():
    spy = SpyEvents()
    spy_dead_letter_store = SpyEvents()
    logger = FakeLogger()

    def assert_consumer(event: Event) -> Result[bool, Error]:
        spy.append(event)
        return isSuccess

    def assert_dead_letter_store_consumer(event: Event) -> Result[bool, Error]:
        spy_dead_letter_store.append(event)
        return isSuccess

    configurer = RabbitMqEventConfigurerMother.with_main_and_retry_ttl_10ms()
    configurer.configure()

    bus = RabbitMqEventBusMother.default()

    event_ids = []
    for _ in range(5):
        event = EventUserCreatedMother.random()
        event_ids.append(event.event_id)
        bus.publish(event)

    max_retries_allowed = 5
    chaos = RabbitMqEventChaos(percentage_simulate_nack=1.0)
    consumer_with_chaos = RabbitMqEventConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer_with_chaos.add_handler_on_store(assert_consumer)
    consumer_with_chaos.start()
    sleep(1.0)
    consumer_with_chaos.stop()

    consumer_without_chaos = RabbitMqEventConsumerMother.default()
    consumer_without_chaos.add_handler_on_queue(
        "dead_letter.store", assert_dead_letter_store_consumer
    )

    consumer_without_chaos.start()
    sleep(1.0)
    consumer_without_chaos.stop()

    configurer.clear()

    for event_id in event_ids:
        spy.assert_count_by_event_id(event_id, 0)  # Rejected before by Event Chaos
        spy_dead_letter_store.assert_count_by_event_id(event_id, 1)
