import os

from typing import Dict

from dataclasses import dataclass
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from petisco.application.singleton import Singleton


@dataclass
class RabbitMQEnvConfig(metaclass=Singleton):
    user: str
    password: str
    host: str
    port: str
    mode: str
    connections: Dict[str, BlockingConnection]

    def __init__(self):
        self.user = os.environ.get("RABBITMQ_USER", "guest")
        self.password = os.environ.get("RABBITMQ_PASSWORD", "guest")
        self.host = os.environ.get("RABBITMQ_HOST", "localhost")
        self.port = os.environ.get("RABBITMQ_PORT", "5672")
        self.connections = {}

    def create_connection(self, key: str):
        blocking_connection = BlockingConnection(
            ConnectionParameters(
                host=self.host,
                port=int(self.port),
                credentials=PlainCredentials(
                    username=self.user, password=self.password
                ),
            )
        )
        self.connections[key] = blocking_connection

    @staticmethod
    def get_connection(key: str):
        rabbitmq_env_config = RabbitMQEnvConfig()
        rabbitmq_env_config.create_connection(key)
        return rabbitmq_env_config.connections.get(key)
