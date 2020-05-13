import os

from pika import BlockingConnection


def create_exchange_and_bind_queue(
    connection: BlockingConnection,
    exchange: str,
    queue: str,
    binding_key: str,
    dead_letter=False,
):
    queue_arguments = {}
    if dead_letter:
        # Note: If queue is already created with another RABBITMQ_MESSAGE_TTL, it will fail.
        message_ttl = int(os.environ.get("RABBITMQ_MESSAGE_TTL", "1000"))  # 1 second
        queue_arguments = {
            "x-message-ttl": message_ttl,
            "x-dead-letter-exchange": f"dlx-{exchange}",
        }

    try:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type="topic", durable=True)
        result = channel.queue_declare(
            queue=queue, durable=True, arguments=queue_arguments
        )
        channel.queue_bind(
            exchange=exchange, queue=result.method.queue, routing_key=binding_key
        )
        channel.close()
    except Exception as error:
        raise TypeError(
            f"RabbitMQEventPublisher: Cannot create the exchange ({exchange}) and bind to queue ({queue}) using given routing_key ({binding_key}) \n{error}"
        )


def create_dead_letter_exchange_and_bind_queue(
    connection: BlockingConnection, exchange: str, queue: str, binding_key: str
):
    channel = connection.channel()

    exchange = f"dlx-{exchange}"
    queue = f"dl-{queue}"

    channel.exchange_declare(exchange=exchange, exchange_type="topic")

    result = channel.queue_declare(queue=queue)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange, routing_key=binding_key, queue=queue_name)
    channel.close()
