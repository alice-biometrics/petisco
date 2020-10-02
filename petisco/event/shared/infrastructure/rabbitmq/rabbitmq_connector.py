import os
import time

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import StreamLostError

from petisco.application.singleton import Singleton


class RabbitMqConnector(metaclass=Singleton):
    def __init__(self):
        self.heartbeat = os.environ.get("RABBITMQ_HEARTBEAT", 60)
        self.user = os.environ.get("RABBITMQ_USER", "guest")
        self.password = os.environ.get("RABBITMQ_PASSWORD", "guest")
        self.host = os.environ.get("RABBITMQ_HOST", "localhost")
        self.port = os.environ.get("RABBITMQ_PORT", "5672")
        self.num_max_retries_connection = os.environ.get(
            "RABBITMQ_CONNECTION_NUM_MAX_RETRIES", 15
        )
        self.wait_seconds_retry = os.environ.get(
            "RABBITMQ_CONNECTION_WAIT_SECONDS_RETRY", 1
        )
        self.open_connections = {}

    def get_connection(self, key_connection: str):
        connection = self.open_connections.get(key_connection)

        if not connection or not connection.is_open:
            connection = self._create_connection(key_connection)

        return connection

    def get_channel(self, key_connection: str) -> BlockingChannel:
        connection = self.get_connection(key_connection)
        try:
            channel = connection.channel()
        except StreamLostError:
            connection = self.get_connection(key_connection)
            channel = connection.channel()
        return channel

    def _create_connection(self, key_connection: str):

        connection = self._create_blocking_connection()

        self._wait_for_open_connection(connection, key_connection)

        if not connection.is_open:
            time_elapsed = round(
                (self.wait_seconds_retry * self.num_max_retries_connection), 2
            )
            raise ConnectionError(
                f"RabbitMQConnector: Impossible to obtain a open connection with host {self.host}. "
                f"Retried {self.num_max_retries_connection} in ~{time_elapsed} seconds"
            )

        return connection

    def _create_blocking_connection(self):
        try:
            connection = BlockingConnection(
                ConnectionParameters(
                    heartbeat=self.heartbeat,
                    host=self.host,
                    port=int(self.port),
                    credentials=PlainCredentials(
                        username=self.user, password=self.password
                    ),
                )
            )
        except:  # noqa E722
            raise ConnectionError(
                f"RabbitMQConnector: Impossible to connect to host {self.host}. "
                f"Review the following envars: [RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_CONNECTION_NUM_MAX_RETRIES, RABBITMQ_CONNECTION_WAIT_SECONDS_RETRY]"
            )
        return connection

    def _wait_for_open_connection(self, connection, key_connection):
        for i in range(self.num_max_retries_connection):
            if connection.is_open:
                self.open_connections[key_connection] = connection
                break
            time.sleep(self.wait_seconds_retry)
