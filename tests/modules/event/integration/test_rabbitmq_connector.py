from unittest import mock
from unittest.mock import PropertyMock

import pytest
from pika import BlockingConnection

from petisco import RabbitMqConnector

from petisco.fixtures import testing_with_rabbitmq


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_get_an_open_connection():

    connector = RabbitMqConnector()

    connection = connector.get_connection("test")

    assert connection.is_open

    connection.close()


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_throw_a_connection_error_exception_when_input_envvars_are_not_valid():

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
def test_should_throw_a_connection_error_exception_when_retries_and_is_not_possible_to_obtain_an_open_connection():

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
def test_should_recover_from_connection_closed():

    connector = RabbitMqConnector()

    connection = connector.get_connection("test")
    connection.close()

    connection = connector.get_connection("test")

    assert connection.is_open

    connection.close()
