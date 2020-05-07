import pytest

from petisco.events.rabbitmq.rabbitmq_connector import RabbitMQConnector
from petisco.events.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)

from petisco.events.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)
from petisco.events.subscriber.infrastructure.rabbitmq_event_subscriber import (
    RabbitMQEventSubscriber,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_subscriber_and_then_unsubscribe_all():

    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={
            "auth": ConfigEventSubscriber(
                organization="acme",
                service="auth",
                topic="auth-events",
                handler=lambda ch, method, properties, body: None,
            )
        },
    )
    subscriber.subscribe_all()

    subscriber.unsubscribe_all()


@pytest.mark.integration
@pytest.mark.skipif(
    not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
)
def test_should_create_a_rabbitmq_event_subscriber_and_then_unsubscribe_all_when_not_subscribe_all_befor():

    subscriber = RabbitMQEventSubscriber(
        connector=RabbitMQConnector(),
        subscribers={
            "auth": ConfigEventSubscriber(
                organization="acme",
                service="auth",
                topic="auth-events",
                handler=lambda ch, method, properties, body: None,
            )
        },
    )
    subscriber.unsubscribe_all()


@pytest.mark.integration
def test_should_fail_subscriber_when_connection_parameter_are_not_valid():
    with pytest.raises(TypeError):
        _ = RabbitMQEventSubscriber(
            connector=None,
            subscribers={
                "auth": ConfigEventSubscriber(
                    organization="acme",
                    service="auth",
                    topic="auth-events",
                    handler=lambda ch, method, properties, body: None,
                )
            },
        )
