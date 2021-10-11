from time import sleep

import pytest
from meiga import BoolResult, isSuccess

from petisco import DomainEvent
from petisco.extra.rabbitmq import RabbitMqMessageChaos
from petisco.legacy import DEBUG
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.rabbitmq.mother.fake_logger import FakeLogger
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
from tests.modules.extra.rabbitmq.utils.assertions import (
    assert_logger_represents_simulated_failure_scenario,
)
from tests.modules.extra.rabbitmq.utils.spy_messages import SpyMessages
from tests.modules.extra.testing_decorators import testing_with_rabbitmq


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_consumer_react_to_default_no_chaos():
    spy = SpyMessages()
    logger = FakeLogger()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    max_retries_allowed = 5
    chaos = RabbitMqMessageChaos()
    consumer = RabbitMqMessageConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_messages(1)
    spy.assert_first_message(domain_event)
    spy.assert_count_by_message_id(domain_event.message_id, 1)

    assert len(logger.get_logging_messages()) == 2
    logging_message = logger.get_logging_messages()[1]
    assert logging_message[0] == DEBUG
    assert logging_message[1]["data"]["message"]["derived_action"] == {
        "action": None,
        "exchange_name": None,
        "routing_key": None,
        "headers": None,
    }


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_works_as_expected_with_chaos_with_zero_probability():
    spy = SpyMessages()
    logger = FakeLogger()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    max_retries_allowed = 5
    chaos = RabbitMqMessageChaos(
        percentage_simulate_nack=0.0, percentage_simulate_failures=0.0
    )
    consumer = RabbitMqMessageConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()

    spy.assert_number_unique_messages(1)
    spy.assert_first_message(domain_event)
    spy.assert_count_by_message_id(domain_event.message_id, 1)

    assert len(logger.get_logging_messages()) == 2
    logging_message = logger.get_logging_messages()[1]
    assert logging_message[0] == DEBUG
    assert logging_message[1]["data"]["message"]["derived_action"] == {
        "action": None,
        "exchange_name": None,
        "routing_key": None,
        "headers": None,
    }


@pytest.mark.integration
@testing_with_rabbitmq
@pytest.mark.parametrize(
    "max_retries_allowed,expected_number_event_consumed,chaos",
    [
        (5, 0, RabbitMqMessageChaos(percentage_simulate_nack=1.0)),
        (1, 0, RabbitMqMessageChaos(percentage_simulate_failures=1.0)),
        (1, 1, RabbitMqMessageChaos(delay_before_event_handler_second=2.0)),
    ],
)
def test_message_consumer_should_works_when_configure_several_chaos_inputs(
    max_retries_allowed, expected_number_event_consumed, chaos
):
    spy = SpyMessages()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    consumer = RabbitMqMessageConsumerMother.with_chaos(chaos, max_retries_allowed)
    consumer.add_subscribers(subscribers)
    consumer.start()

    sleep(1.0)

    consumer.stop()
    configurer.clear()
    spy.assert_count_by_message_id(
        domain_event.message_id, expected_number_event_consumed
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_works_when_chaos_is_configurer_with_nck_simulation_and_check_logger():
    spy = SpyMessages()
    logger = FakeLogger()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_retry_ttl_10ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    max_retries_allowed = 5
    chaos = RabbitMqMessageChaos(percentage_simulate_nack=1.0)
    consumer = RabbitMqMessageConsumerMother.with_chaos(
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
        "layer": "rabbitmq_message_consumer",
        "operation": "handle",
    }
    assert (
        first_logging_message[1]["data"]["message"]["chaos_action"] == "nack simulated"
    )


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_works_when_chaos_is_configure_with_failure_simulation_and_check_logger_without_subscribers():
    spy = SpyMessages()
    spy_dead_letter = SpyMessages()

    logger = FakeLogger()

    def assert_store_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    def assert_dead_letter_store_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()

    configurer = RabbitMqMessageConfigurerMother.with_main_and_retry_ttl_100ms()
    configurer.configure()

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    max_retries_allowed = 5
    chaos = RabbitMqMessageChaos(
        percentage_simulate_failures=1.0, protected_routing_keys=["dead_letter.store"]
    )
    consumer = RabbitMqMessageConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(
        [MessageSubscriberMother.all_messages_subscriber(handler=assert_store_consumer)]
    )
    consumer.add_subscriber_on_queue(
        "dead_letter.store",
        MessageSubscriberMother.all_messages_subscriber(
            handler=assert_dead_letter_store_consumer
        ),
    )
    consumer.start()

    sleep(1.5)

    consumer.stop()
    configurer.clear()

    spy.assert_count_by_message_id(domain_event.message_id, 0)
    spy_dead_letter.assert_count_by_message_id(domain_event.message_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_works_when_chaos_is_configured_with_failure_simulation_and_check_logger_with_subscribers():
    spy = SpyMessages()
    spy_dead_letter = SpyMessages()

    logger = FakeLogger()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy.append(domain_event)
        return isSuccess

    def assert_dead_letter_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        )
    ]

    configurer = RabbitMqMessageConfigurerMother.with_main_and_retry_ttl_100ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    max_retries_allowed = 5
    chaos = RabbitMqMessageChaos(
        percentage_simulate_failures=1.0,
        protected_routing_keys=[
            "dead_letter.alice.petisco.1.event.user_created.my_domain_event_subscriber"
        ],
    )
    consumer = RabbitMqMessageConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.add_subscriber_on_queue(
        queue_name="dead_letter.alice.petisco.1.event.user_created.my_domain_event_subscriber",
        subscriber=MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_dead_letter_consumer
        ),
    )

    consumer.start()

    sleep(1.5)

    consumer.stop()
    configurer.clear()

    spy.assert_count_by_message_id(domain_event.message_id, 0)
    spy_dead_letter.assert_count_by_message_id(domain_event.message_id, 1)

    assert_logger_represents_simulated_failure_scenario(logger, max_retries_allowed)


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_consumer_react_to_chaos_with_failure_simulation_on_store_and_subscriber_queue():
    spy_subscriber = SpyMessages()
    spy_store = SpyMessages()
    spy_dead_letter_subscriber = SpyMessages()
    spy_dead_letter_store = SpyMessages()

    logger = FakeLogger()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_subscriber.append(domain_event)
        return isSuccess

    def assert_store_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_store.append(domain_event)
        return isSuccess

    def assert_dead_letter_subscriber_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter_subscriber.append(domain_event)
        return isSuccess

    def assert_dead_letter_store_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter_store.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        ),
        MessageSubscriberMother.all_messages_subscriber(handler=assert_store_consumer),
    ]

    configurer = RabbitMqMessageConfigurerMother.with_main_and_retry_ttl_100ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    max_retries_allowed = 5
    chaos = RabbitMqMessageChaos(
        percentage_simulate_failures=1.0,
        protected_routing_keys=[
            "dead_letter.alice.petisco.1.event.user_created.my_domain_event_subscriber",
            "dead_letter.store",
        ],
    )
    consumer = RabbitMqMessageConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.add_subscriber_on_queue(
        queue_name="dead_letter.alice.petisco.1.event.user_created.my_domain_event_subscriber",
        subscriber=MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event),
            handler=assert_dead_letter_subscriber_consumer,
        ),
    )
    consumer.add_subscriber_on_queue(
        queue_name="dead_letter.store",
        subscriber=MessageSubscriberMother.other_all_messages_subscriber(
            handler=assert_dead_letter_store_consumer
        ),
    )

    consumer.start()

    sleep(1.5)

    consumer.stop()
    configurer.clear()

    spy_subscriber.assert_count_by_message_id(domain_event.message_id, 0)
    spy_store.assert_count_by_message_id(domain_event.message_id, 0)

    spy_dead_letter_subscriber.assert_count_by_message_id(domain_event.message_id, 1)
    spy_dead_letter_store.assert_count_by_message_id(domain_event.message_id, 1)


@pytest.mark.integration
@testing_with_rabbitmq
def test_message_consumer_should_consumer_react_to_chaos_with_failure_simulation_only_on_subscriber_queue():
    spy_subscriber = SpyMessages()
    spy_store = SpyMessages()
    spy_dead_letter_subscriber = SpyMessages()
    spy_dead_letter_store = SpyMessages()

    logger = FakeLogger()

    def assert_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_subscriber.append(domain_event)
        return isSuccess

    def assert_store_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_store.append(domain_event)
        return isSuccess

    def assert_dead_letter_subscriber_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter_subscriber.append(domain_event)
        return isSuccess

    def assert_dead_letter_store_consumer(domain_event: DomainEvent) -> BoolResult:
        spy_dead_letter_store.append(domain_event)
        return isSuccess

    domain_event = DomainEventUserCreatedMother.random()
    subscribers = [
        MessageSubscriberMother.domain_event_subscriber(
            domain_event_type=type(domain_event), handler=assert_consumer
        ),
        MessageSubscriberMother.all_messages_subscriber(handler=assert_store_consumer),
    ]

    configurer = RabbitMqMessageConfigurerMother.with_main_and_retry_ttl_100ms()
    configurer.configure_subscribers(subscribers)

    bus = RabbitMqDomainEventBusMother.default()
    bus.publish(domain_event)

    max_retries_allowed = 5
    chaos = RabbitMqMessageChaos(
        percentage_simulate_failures=1.0,
        protected_routing_keys=[
            "dead_letter.alice.petisco.1.event.user_created.my_domain_event_subscriber",
            "dead_letter.store",
            "store",
        ],
    )
    consumer = RabbitMqMessageConsumerMother.with_chaos(
        chaos, max_retries_allowed, logger
    )
    consumer.add_subscribers(subscribers)
    consumer.add_subscriber_on_queue(
        queue_name="dead_letter.alice.petisco.1.event.user_created.my_domain_event_subscriber",
        subscriber=MessageSubscriberMother.other_domain_event_subscriber(
            domain_event_type=type(domain_event),
            handler=assert_dead_letter_subscriber_consumer,
        ),
    )
    consumer.add_subscriber_on_queue(
        queue_name="dead_letter.store",
        subscriber=MessageSubscriberMother.other_all_messages_subscriber(
            handler=assert_dead_letter_store_consumer
        ),
    )

    consumer.start()

    sleep(1.5)

    consumer.stop()
    configurer.clear()

    spy_subscriber.assert_count_by_message_id(domain_event.message_id, 0)
    spy_store.assert_count_by_message_id(domain_event.message_id, 1)
    spy_dead_letter_subscriber.assert_count_by_message_id(domain_event.message_id, 1)
    spy_dead_letter_store.assert_count_by_message_id(domain_event.message_id, 0)


#
# def assert_logger_represents_simulated_failure_scenario(logger, max_retries_allowed):
#     def assert_redelivered_message(
#         logging_message, expected_derived_action, check_headers: bool
#     ):
#         assert logging_message[0] == DEBUG
#         assert logging_message[1]["meta"] == {
#             "layer": "rabbitmq_event_consumer",
#             "operation": "assert_consumer",
#         }
#         assert logging_message[1]["data"]["message"]["result"] == Failure(
#             EventChaosError()
#         )
#         derived_action = logging_message[1]["data"]["message"]["derived_action"]
#
#         if check_headers:
#             derived_action["headers"].pop("x-death")
#             derived_action["headers"].pop("x-first-death-exchange")
#             derived_action["headers"].pop("x-first-death-queue")
#             derived_action["headers"].pop("x-first-death-reason")
#
#         assert derived_action == expected_derived_action
#
#     def assert_send_to_retry(logging_message, redelivery_count, check_headers):
#         expected_derived_action = {
#             "action": "send_to_retry",
#             "exchange_name": "retry.alice.petisco",
#             "routing_key": "retry.alice.petisco.1.event.user_created.assert_consumer",
#             "headers": {
#                 "queue": "alice.petisco.1.event.user_created.assert_consumer",
#                 "redelivery_count": redelivery_count,
#             },
#         }
#         assert_redelivered_message(
#             logging_message, expected_derived_action, check_headers
#         )
#
#     def assert_send_to_dead_leter(logging_message, redelivery_count, check_headers):
#         expected_derived_action = {
#             "action": "send_to_dead_letter",
#             "exchange_name": "dead_letter.alice.petisco",
#             "routing_key": "dead_letter.alice.petisco.1.event.user_created.assert_consumer",
#             "headers": {
#                 "queue": "alice.petisco.1.event.user_created.assert_consumer",
#                 "redelivery_count": redelivery_count,
#             },
#         }
#         assert_redelivered_message(
#             logging_message, expected_derived_action, check_headers
#         )
#
#     def assert_failure_simulator(logging_message):
#         assert (
#             logging_message[1]["data"]["message"]["chaos_action"] == "failure simulated"
#         )
#
#     # filter received_message logs
#     logging_messages = [
#         log_message
#         for log_message in logger.get_logging_messages()
#         if "log_activity" not in log_message[1]["data"]["message"]
#         or log_message[1]["data"]["message"]["log_activity"] != "received_message"
#     ]
#
#     assert_send_to_retry(logging_messages[1], 1, False)
#
#     redelivered_count = 2
#     for i in range(3, 10, 2):
#         assert_send_to_retry(logging_messages[i], redelivered_count, True)
#         redelivered_count += 1
#
#     for i in range(2, 10, 2):
#         assert_failure_simulator(logging_messages[i])
#
#     assert_send_to_dead_leter(logging_messages[-2], 6, True)
#
#
# @pytest.mark.integration
# @testing_with_rabbitmq
# def test_message_consumer_should_consumer_react_to_chaos_with_nck_simulation_and_send_event_to_dead_letter():
#     spy = SpyEvents()
#     spy_dead_letter = SpyEvents()
#     spy_dead_letter_store = SpyEvents()
#     logger = FakeLogger()
#
#     def assert_consumer(event: Event) -> Result[bool, Error]:
#         spy.append(event)
#         return isSuccess
#
#     def assert_dead_letter_consumer(event: Event) -> Result[bool, Error]:
#         spy_dead_letter.append(event)
#         return isSuccess
#
#     def assert_dead_letter_store_consumer(event: Event) -> Result[bool, Error]:
#         spy_dead_letter_store.append(event)
#         return isSuccess
#
#     event = EventUserCreatedMother.random()
#     subscribers = [
#         EventSubscriber(
#             event_name=event.event_name,
#             event_version=event.event_version,
#             handlers=[assert_consumer],
#         )
#     ]
#
#     configurer = RabbitMqEventConfigurerMother.with_main_and_retry_ttl_10ms()
#     configurer.configure_subscribers(subscribers)
#
#     bus = RabbitMqEventBusMother.default()
#     bus.publish(event)
#
#     max_retries_allowed = 5
#     chaos = RabbitMqEventChaos(percentage_simulate_nack=1.0)
#     consumer_with_chaos = RabbitMqEventConsumerMother.with_chaos(
#         chaos, max_retries_allowed, logger
#     )
#     consumer_with_chaos.add_subscribers(subscribers)
#     consumer_with_chaos.start()
#     sleep(1.0)
#     consumer_with_chaos.stop()
#
#     consumer_without_chaos = RabbitMqEventConsumerMother.default()
#     consumer_without_chaos.add_handler_on_queue(
#         "dead_letter.alice.petisco.1.event.user_created.assert_consumer",
#         assert_dead_letter_consumer,
#     )
#     consumer_without_chaos.add_handler_on_queue(
#         "dead_letter.store", assert_dead_letter_store_consumer
#     )
#
#     consumer_without_chaos.start()
#     sleep(1.0)
#     consumer_without_chaos.stop()
#
#     configurer.clear()
#
#     spy.assert_count_by_event_id(event.event_id, 0)  # Rejected before by Event Chaos
#     spy_dead_letter.assert_count_by_event_id(event.event_id, 1)
#     spy_dead_letter_store.assert_count_by_event_id(event.event_id, 1)
#
#
# @pytest.mark.integration
# @testing_with_rabbitmq
# def test_message_consumer_should_store_consumer_react_to_chaos_with_nck_simulation_and_send_several_event_to_dead_letter():
#     spy = SpyEvents()
#     spy_dead_letter_store = SpyEvents()
#     logger = FakeLogger()
#
#     def assert_consumer(event: Event) -> Result[bool, Error]:
#         spy.append(event)
#         return isSuccess
#
#     def assert_dead_letter_store_consumer(event: Event) -> Result[bool, Error]:
#         spy_dead_letter_store.append(event)
#         return isSuccess
#
#     configurer = RabbitMqEventConfigurerMother.with_main_and_retry_ttl_10ms()
#     configurer.configure()
#
#     bus = RabbitMqEventBusMother.default()
#
#     event_ids = []
#     for _ in range(5):
#         event = EventUserCreatedMother.random()
#         event_ids.append(event.event_id)
#         bus.publish(event)
#
#     max_retries_allowed = 5
#     chaos = RabbitMqEventChaos(percentage_simulate_nack=1.0)
#     consumer_with_chaos = RabbitMqEventConsumerMother.with_chaos(
#         chaos, max_retries_allowed, logger
#     )
#     consumer_with_chaos.add_handler_on_store(assert_consumer)
#     consumer_with_chaos.start()
#     sleep(1.0)
#     consumer_with_chaos.stop()
#
#     consumer_without_chaos = RabbitMqEventConsumerMother.default()
#     consumer_without_chaos.add_handler_on_queue(
#         "dead_letter.store", assert_dead_letter_store_consumer
#     )
#
#     consumer_without_chaos.start()
#     sleep(1.0)
#     consumer_without_chaos.stop()
#
#     configurer.clear()
#
#     for event_id in event_ids:
#         spy.assert_count_by_event_id(event_id, 0)  # Rejected before by Event Chaos
#         spy_dead_letter_store.assert_count_by_event_id(event_id, 1)
