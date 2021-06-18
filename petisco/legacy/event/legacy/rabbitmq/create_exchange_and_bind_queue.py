import os

from pika.adapters.blocking_connection import BlockingChannel


def create_exchange_and_bind_queue(
    channel: BlockingChannel,
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
        channel.exchange_declare(exchange=exchange, exchange_type="topic", durable=True)
        result = channel.queue_declare(
            queue=queue, arguments=queue_arguments, durable=True
        )
        channel.queue_bind(
            exchange=exchange, queue=result.method.queue, routing_key=binding_key
        )
    except Exception as error:
        raise TypeError(
            f"RabbitMQEventPublisher: Cannot create the exchange ({exchange}) and bind to queue ({queue}) using given routing_key ({binding_key}) \n{error}"
        )


def create_dead_letter_exchange_and_bind_queue(
    channel: BlockingChannel, exchange: str, queue: str, binding_key: str
):
    exchange = f"dlx-{exchange}"
    queue = f"dl-{queue}"

    channel.exchange_declare(exchange=exchange, exchange_type="topic", durable=True)

    result = channel.queue_declare(queue=queue, durable=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange, routing_key=binding_key, queue=queue_name)
