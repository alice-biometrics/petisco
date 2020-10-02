import pytest

from petisco import RabbitMqConnector

from petisco.fixtures.testing_decorators import testing_with_rabbitmq
from tests.modules.event.mothers.defaults import DEFAULT_EXCHANGE_NAME
from tests.modules.event.mothers.rabbitmq_event_bus_mother import RabbitMqEventBusMother
from tests.modules.event.mothers.rabbitmq_event_configurer_mother import (
    RabbitMqEventConfigurerMother,
)


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_recover_from_connection_error_when_publish_an_event(
    make_user_created_event,
):
    connector = RabbitMqConnector()
    original_wait_seconds_retry = connector.wait_seconds_retry
    connector.wait_seconds_retry = 0.1

    configurer = RabbitMqEventConfigurerMother.default(connector)

    event = make_user_created_event()

    configurer.configure_event(event)

    bus = RabbitMqEventBusMother.default(connector)

    connection = connector.get_connection(DEFAULT_EXCHANGE_NAME)

    connection.close()

    bus.publish(event)

    connector.wait_seconds_retry = original_wait_seconds_retry

    configurer.clear()
