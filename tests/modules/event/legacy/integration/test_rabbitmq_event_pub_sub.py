from time import sleep

import pytest
from meiga import isSuccess, isFailure

from petisco import (
    Event,
    subscriber_handler,
    RabbitMQEventPublisher,
    RabbitMQEventSubscriber,
    ConfigEventSubscriber,
    RabbitMqConnector,
)
from petisco.fixtures import testing_with_rabbitmq
from tests.fixtures import TrackedEventsSpy


def await_for_events():
    sleep(1.5)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_work_successfully_a_happy_path_pub_sub(
    given_any_petisco,
    make_user_created_event,
    given_random_organization,
    given_random_service,
    given_random_topic,
):
    event_1 = make_user_created_event()
    event_2 = make_user_created_event()

    tracked_events_spy = TrackedEventsSpy()

    @subscriber_handler()
    def main_handler(event: Event):
        tracked_events_spy.append(event)
        return isSuccess

    publisher = RabbitMQEventPublisher(
        connector=RabbitMqConnector(),
        organization=given_random_organization,
        service=given_random_service,
        topic=given_random_topic,
    )

    publisher.publish_events([event_1, event_2])

    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMqConnector(),
        subscribers={
            "auth": ConfigEventSubscriber(
                organization=given_random_organization,
                service=given_random_service,
                topic=given_random_topic,
                handler=main_handler,
            )
        },
    )
    subscriber.start()

    await_for_events()

    tracked_events_spy.assert_number_events(2)

    subscriber.stop()


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_publish_reject_and_requeue_from_dead_letter_exchange(
    given_any_petisco,
    make_user_created_event,
    given_random_organization,
    given_random_service,
    given_random_topic,
    given_a_short_message_ttl,
):
    event = make_user_created_event()
    tracked_events_spy = TrackedEventsSpy()
    tracked_requeue_events_dead_letter_spy = TrackedEventsSpy()

    publisher = RabbitMQEventPublisher(
        connector=RabbitMqConnector(),
        organization=given_random_organization,
        service=given_random_service,
        topic=given_random_topic,
    )

    @subscriber_handler()
    def main_handler(event: Event):
        tracked_events_spy.append(event)
        return isFailure

    @subscriber_handler()
    def requeue_from_dead_letter(event: Event):
        tracked_requeue_events_dead_letter_spy.append(event)
        publisher.publish(event)
        return isSuccess

    publisher.publish(event)

    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMqConnector(),
        subscribers={
            "auth": ConfigEventSubscriber(
                organization=given_random_organization,
                service=given_random_service,
                topic=given_random_topic,
                handler=main_handler,
            ),
            "dead-letter": ConfigEventSubscriber(
                organization=given_random_organization,
                service=given_random_service,
                topic=given_random_topic,
                handler=requeue_from_dead_letter,
                dead_letter=True,
            ),
        },
    )
    subscriber.start()

    await_for_events()

    tracked_events_spy.assert_number_events(1)
    tracked_requeue_events_dead_letter_spy.assert_number_events(1)

    subscriber.stop()


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_work_successfully_a_happy_path_pub_sub_with_subscribers_simulations_nack_everything(
    given_any_petisco,
    make_user_created_event,
    given_random_organization,
    given_random_service,
    given_random_topic,
):
    event = make_user_created_event()
    tracked_events_spy = TrackedEventsSpy()

    @subscriber_handler(percentage_simulate_nack=1.0)
    def main_handler_everything_nack(event: Event):
        tracked_events_spy.append(event)
        return isSuccess

    publisher = RabbitMQEventPublisher(
        connector=RabbitMqConnector(),
        organization=given_random_organization,
        service=given_random_service,
        topic=given_random_topic,
    )

    publisher.publish_events([event, event])

    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMqConnector(),
        subscribers={
            "auth": ConfigEventSubscriber(
                organization=given_random_organization,
                service=given_random_service,
                topic=given_random_topic,
                handler=main_handler_everything_nack,
            )
        },
    )
    subscriber.start()

    await_for_events()

    tracked_events_spy.assert_number_events(0)

    subscriber.stop()
