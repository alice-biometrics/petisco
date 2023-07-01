from unittest import mock
from unittest.mock import PropertyMock, patch

import pytest
from pika import BlockingConnection
from pika.exceptions import ConnectionClosedByBroker

from petisco.extra.rabbitmq import RabbitMqConnector
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
from tests.modules.extra.testing_decorators import (
    testing_with_rabbitmq,
    testing_without_rabbitmq,
)


@pytest.mark.integration
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
class TestRabbitMqConnector:
    @testing_with_rabbitmq
    def should_ping_with_available_rabbitmq(self):
        RabbitMqConnector.ping()

    @testing_without_rabbitmq
    def should_raise_an_exception_when_connection_with_rabbitmq_is_not_available(self):
        with pytest.raises(ConnectionError):
            RabbitMqConnector.ping()

    @testing_with_rabbitmq
    def should_get_an_open_connection(self):
        connector = RabbitMqConnector()

        connection = connector.get_connection("test")

        assert connection.is_open

        connection.close()

        connector.close("test")

        assert "test" not in connector.open_connections

    @testing_with_rabbitmq
    def should_raise_a_connection_error_exception_when_input_envvars_are_not_valid(
        self,
    ):
        connector = RabbitMqConnector()
        original_host = connector.host
        connector.host = "invalid"

        with pytest.raises(
            ConnectionError, match="RabbitMQConnector: Impossible to connect to host*"
        ):
            connector.get_connection("test")

        connector.host = original_host

    @testing_with_rabbitmq
    def should_raise_a_connection_error_exception_when_retries_and_is_not_possible_to_obtain_an_open_connection(
        self,
    ):
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

    @testing_with_rabbitmq
    def should_recover_from_connection_closed(self):
        connector = RabbitMqConnector()

        connection = connector.get_connection("test")
        connection.close()

        connection = connector.get_connection("test")

        assert connection.is_open

        connection.close()

    @testing_with_rabbitmq
    def should_recover_channel_when_connection_has_been_closed_by_broker(self):
        connector = RabbitMqConnector()

        valid_channel = connector.get_channel("valid_channel")

        with patch(
            "pika.BlockingConnection.channel",
            side_effect=[ConnectionClosedByBroker(1, ""), valid_channel],
        ):
            connection = connector.get_channel("test")

        assert connection.is_open

        connection.close()

    @testing_with_rabbitmq
    def should_recover_from_connection_error_when_publish_an_event(self):
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

    @testing_with_rabbitmq
    def should_close_all_connections(self):
        connector = RabbitMqConnector()

        for key_connection in ["key1", "key2", "key3"]:
            connection = connector.get_connection(key_connection)
            assert connection.is_open

        connector.close_all()

        assert connector.open_connections == dict()
