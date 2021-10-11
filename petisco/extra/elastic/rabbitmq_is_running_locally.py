def rabbitmq_is_running_locally() -> bool:
    try:
        import pika  # noqa: F401

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        is_running_locally = connection.is_open
        connection.close()
        return is_running_locally
    except:  # noqa: E722
        return False
