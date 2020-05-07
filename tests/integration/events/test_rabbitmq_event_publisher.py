import pytest

from petisco.events.publisher.infrastructure.rabbitmq_event_publisher import (
    RabbitMQEventPublisher,
)
from petisco.events.rabbitmq.rabbitmq_connector import RabbitMQConnector
from petisco.events.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_publisher_and_publish_a_event(
    make_user_created_event
):
    event = make_user_created_event()

    publisher = RabbitMQEventPublisher(
        connector=RabbitMQConnector(),
        organization="acme",
        service="service",
        topic="service-events",
    )

    publisher.publish(event)


@pytest.mark.integration
def test_should_fail_publisher_when_connection_parameter_are_not_valid():
    with pytest.raises(TypeError):
        _ = RabbitMQEventPublisher(
            connector=None,
            organization="acme",
            service="service",
            topic="service-events",
        )
