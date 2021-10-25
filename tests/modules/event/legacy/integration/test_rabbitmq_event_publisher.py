from time import sleep

import pytest

from petisco.event.legacy.publisher.infrastructure.rabbitmq_event_publisher import (
    RabbitMQEventPublisher,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
    RabbitMqConnector,
)
from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_publisher_and_publish_a_event(
    make_user_created_event,
):
    rabbitmq_connector = RabbitMqConnector()
    event = make_user_created_event()

    publisher = RabbitMQEventPublisher(
        connector=rabbitmq_connector,
        organization="acme",
        service="service",
        topic="service-event",
    )

    publisher.publish(event)


@pytest.mark.integration
def test_should_fail_publisher_when_connection_parameter_are_not_valid():
    with pytest.raises(TypeError):
        _ = RabbitMQEventPublisher(
            connector=None,
            organization="acme",
            service="service",
            topic="service-event",
        )


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_publisher_and_publish_a_event_after_heartbeat(
    make_user_created_event,
):
    event = make_user_created_event()
    rabbitmq_connector = RabbitMqConnector()
    rabbitmq_connector.heartbeat = 2

    publisher = RabbitMQEventPublisher(
        connector=rabbitmq_connector,
        organization="acme",
        service="service",
        topic="service-event",
    )

    sleep(10)  # wait more than the heartbeat

    publisher.publish(event)
