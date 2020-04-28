import os

from dataclasses import dataclass
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from petisco import Singleton


@dataclass
class RabbitMQEnvConfig(metaclass=Singleton):
    user: str
    password: str
    host: str
    port: str
    mode: str

    def __init__(self):
        self.user = os.environ.get("RABBITMQ_USER", "guest")
        self.password = os.environ.get("RABBITMQ_PASSWORD", "guest")
        self.host = os.environ.get("RABBITMQ_HOST", "localhost")
        self.port = os.environ.get("RABBITMQ_PORT", "5672")
        self._setup_connection()

    def _setup_connection(self):
        self.connection = BlockingConnection(
            ConnectionParameters(
                host=self.host,
                port=int(self.port),
                credentials=PlainCredentials(
                    username=self.user, password=self.password
                ),
            )
        )

    @staticmethod
    def get_connection():
        return RabbitMQEnvConfig.get_instance().connection
