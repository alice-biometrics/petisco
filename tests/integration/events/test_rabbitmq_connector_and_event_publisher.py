import pytest

from petisco import RabbitMQConnector, RabbitMQEventPublisher

from petisco.events.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_recover_from_connection_error_when_publish_an_event(
    make_user_created_event,
    given_random_organization,
    given_random_service,
    given_random_topic,
):

    connector = RabbitMQConnector()
    original_wait_seconds_retry = connector.wait_seconds_retry
    connector.wait_seconds_retry = 0.1

    event = make_user_created_event()
    publisher = RabbitMQEventPublisher(
        connector=connector,
        organization=given_random_organization,
        service=given_random_service,
        topic=given_random_topic,
    )
    connection = connector.get_connection(
        f"{given_random_organization}.{given_random_service}"
    )

    connection.close()

    publisher.publish(event)

    connector.wait_seconds_retry = original_wait_seconds_retry
