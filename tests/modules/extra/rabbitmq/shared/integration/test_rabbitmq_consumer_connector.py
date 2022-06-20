import pytest
from pika.adapters.blocking_connection import BlockingChannel

from petisco.extra.rabbitmq import RabbitMqConnector
from petisco.extra.rabbitmq.shared.rabbitmq_consumer_connector import (
    RabbitMqConsumerConnector,
)
from tests.modules.extra.testing_decorators import testing_with_rabbitmq


@pytest.mark.integration
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
class TestRabbitMqConsumerConnector:
    channel: BlockingChannel

    def setup(self):
        base_connector = RabbitMqConnector()
        self.channel = base_connector.get_channel("test-channel")

    @testing_with_rabbitmq
    def should_raise_exception_when_try_to_get_connection(self):
        connector = RabbitMqConsumerConnector(self.channel)

        with pytest.raises(RuntimeError) as excinfo:
            _ = connector.get_connection("test")
        assert "RabbitMqConsumerConnector works only with given channel." in str(
            excinfo.value
        )

    @testing_with_rabbitmq
    def should_get_channel(self):

        connector = RabbitMqConsumerConnector(self.channel)

        channel = connector.get_channel("test-channel")

        assert channel == self.channel
