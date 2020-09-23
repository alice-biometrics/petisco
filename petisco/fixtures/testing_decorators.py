import functools

import pytest

from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)


def testing_with_rabbitmq(func):
    @pytest.mark.skipif(
        not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
