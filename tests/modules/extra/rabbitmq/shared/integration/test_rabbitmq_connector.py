from unittest import mock
from unittest.mock import PropertyMock

import pytest
from pika import BlockingConnection

from petisco.extra.rabbitmq import RabbitMqConnector
from petisco.legacy.fixtures import testing_with_rabbitmq
from tests.modules.extra.rabbitmq.mother.defaults import DEFAULT_EXCHANGE_NAME
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_domain_event_bus_mother import (
    RabbitMqDomainEventBusMother,
)
from tests.modules.extra.rabbitmq.mother.rabbitmq_message_configurer_mother import (
    RabbitMqMessageConfigurerMother,
)


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_connector_should_get_an_open_connection():

    connector = RabbitMqConnector()

    connection = connector.get_connection("test")

    assert connection.is_open

    connection.close()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_connector_should_raise__a_connection_error_exception_when_input_envvars_are_not_valid():

    connector = RabbitMqConnector()
    original_host = connector.host
    connector.host = "invalid"

    with pytest.raises(
        ConnectionError, match="RabbitMQConnector: Impossible to connect to host*"
    ):
        connector.get_connection("test")

    connector.host = original_host


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_connector_should_raise_a_connection_error_exception_when_retries_and_is_not_possible_to_obtain_an_open_connection():

    connector = RabbitMqConnector()
    original_wait_seconds_retry = connector.wait_seconds_retry
    connector.wait_seconds_retry = 0.1

    connection = connector.get_connection("test")
    connection.close()

    with mock.patch.object(
        BlockingConnection, "is_open", new_callable=PropertyMock
    ) as mocker_is_open:
        mocker_is_open.return_value = False
        with pytest.raises(
            ConnectionError,
            match="RabbitMQConnector: Impossible to obtain a open connection with host*",
        ):
            connector.get_connection("test")

    connector.wait_seconds_retry = original_wait_seconds_retry


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_connector_should_recover_from_connection_closed():

    connector = RabbitMqConnector()

    connection = connector.get_connection("test")
    connection.close()

    connection = connector.get_connection("test")

    assert connection.is_open

    connection.close()


@pytest.mark.integration
@testing_with_rabbitmq
def test_rabbitmq_connector_should_recover_from_connection_error_when_publish_an_event():
    connector = RabbitMqConnector()
    original_wait_seconds_retry = connector.wait_seconds_retry
    connector.wait_seconds_retry = 0.1

    configurer = RabbitMqMessageConfigurerMother.default(connector)

    domain_event = DomainEventUserCreatedMother.random()

    configurer.configure()

    bus = RabbitMqDomainEventBusMother.default(connector)

    connection = connector.get_connection(DEFAULT_EXCHANGE_NAME)

    connection.close()

    bus.publish(domain_event)

    connector.wait_seconds_retry = original_wait_seconds_retry

    configurer.clear()
