from pika.adapters.blocking_connection import BlockingChannel


class RabbitMqConsumerConnector:
    def __init__(self, channel: BlockingChannel):
        self.channel = channel

    def get_connection(self, key_connection: str):
        raise RuntimeError("RabbitMqConsumerConnector works only with given channel.")

    def close(self, key_connection: str):
        pass

    def get_channel(self, key_connection: str) -> BlockingChannel:
        return self.channel
