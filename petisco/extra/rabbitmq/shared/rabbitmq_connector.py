import os
import time
from typing import Dict

from loguru import logger
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ConnectionClosedByBroker, StreamLostError

from petisco.base.misc.singleton import Singleton


class RabbitMqConnector(metaclass=Singleton):
    """
    Singleton class to define RabbitMQ connections and some infrastructure configurations.
    """

    def __init__(self) -> None:
        self.heartbeat = int(os.environ.get("RABBITMQ_HEARTBEAT", 60))
        self.user = os.environ.get("RABBITMQ_USER", "guest")
        self.password = os.environ.get("RABBITMQ_PASSWORD", "guest")
        self.host = os.environ.get("RABBITMQ_HOST", "localhost")
        self.port = os.environ.get("RABBITMQ_PORT", "5672")
        self.num_max_retries_connection = int(os.environ.get("RABBITMQ_CONNECTION_NUM_MAX_RETRIES", 15))
        self.wait_seconds_retry = float(os.environ.get("RABBITMQ_CONNECTION_WAIT_SECONDS_RETRY", 1))
        self.prefetch_count = int(os.environ.get("RABBITMQ_PREFETCH_COUNT", 1))
        self.open_connections: Dict[str, BlockingConnection] = {}

    @staticmethod
    def ping() -> None:
        connector = RabbitMqConnector()
        connector.get_connection(key_connection="ping")
        connector.close(key_connection="ping")

    def close_all(self) -> None:
        for key_connection in list(self.open_connections.keys()):
            connection = self.open_connections.pop(key_connection)
            if connection and connection.is_open:
                try:
                    connection.close()
                except StreamLostError as exc:
                    logger.warning(f"close_all: {str(exc)}")
                except Exception as exc:  # noqa
                    logger.error(f"close_all: {str(exc)}")

    def close(self, key_connection: str) -> None:
        connection = self.open_connections.pop(key_connection)
        if connection and connection.is_open:
            try:
                connection.close()
            except StreamLostError as exc:
                logger.warning(f"close: {str(exc)}")
            except Exception as exc:  # noqa
                logger.error(f"close_all: {str(exc)}")

    def get_connection(self, key_connection: str) -> BlockingConnection:
        connection = self.open_connections.get(key_connection)

        if not connection or not connection.is_open:
            connection = self._create_connection(key_connection)

        return connection

    def get_channel(self, key_connection: str) -> BlockingChannel:
        connection = self.get_connection(key_connection)
        try:
            channel = connection.channel()
            channel.basic_qos(prefetch_count=self.prefetch_count, global_qos=True)
            channel.confirm_delivery()
        except StreamLostError:
            connection = self.get_connection(key_connection)
            channel = connection.channel()
            channel.confirm_delivery()
        except ConnectionClosedByBroker:
            del self.open_connections[key_connection]
            connection = self.get_connection(key_connection)
            channel = connection.channel()
            channel.confirm_delivery()
        return channel

    def _create_connection(self, key_connection: str) -> BlockingConnection:
        connection = self._create_blocking_connection(key_connection)

        self._wait_for_open_connection(connection, key_connection)

        if not connection.is_open:
            time_elapsed = round((self.wait_seconds_retry * self.num_max_retries_connection), 2)
            raise ConnectionError(
                f"RabbitMQConnector: Impossible to obtain a open connection with host {self.host}. "
                f"Retried {self.num_max_retries_connection} in ~{time_elapsed} seconds"
            )

        return connection

    def _create_blocking_connection(self, connection_name: str) -> BlockingConnection:
        try:
            connection = BlockingConnection(
                ConnectionParameters(
                    heartbeat=self.heartbeat,
                    host=self.host,
                    port=int(self.port),
                    credentials=PlainCredentials(username=self.user, password=self.password),
                    client_properties={"connection_name": connection_name},
                )
            )
        except Exception as exc:
            raise ConnectionError(
                f"RabbitMQConnector: Impossible to connect to host {self.host}. "
                "Review the following envars: [RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, "
                "RABBITMQ_PORT, RABBITMQ_CONNECTION_NUM_MAX_RETRIES, RABBITMQ_CONNECTION_WAIT_SECONDS_RETRY]"
            ) from exc
        return connection

    def _wait_for_open_connection(self, connection: BlockingConnection, key_connection: str) -> None:
        for _i in range(self.num_max_retries_connection):
            if connection.is_open:
                self.open_connections[key_connection] = connection
                break
            time.sleep(self.wait_seconds_retry)
