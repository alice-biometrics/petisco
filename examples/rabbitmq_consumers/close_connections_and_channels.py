from petisco.extra.rabbitmq import RabbitMqConnector


def close_connections_and_channels() -> None:
    connector = RabbitMqConnector()
    connector.close_all()


if __name__ == "__main__":
    close_connections_and_channels()
