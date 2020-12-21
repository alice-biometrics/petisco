import functools

import pytest

from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_is_running_locally import (
    rabbitmq_is_running_locally,
)
from petisco.persistence.elastic.elastic_is_running_locally import (
    elastic_is_running_locally,
)
from petisco.persistence.sql.mysql_is_running_locally import mysql_is_running_locally


def testing_with_rabbitmq(func):
    @pytest.mark.skipif(
        not rabbitmq_is_running_locally(), reason="RabbitMQ is not running locally"
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def testing_with_mysql(func):
    @pytest.mark.skipif(
        not mysql_is_running_locally(), reason="MySQL is not running locally"
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def testing_with_elastic(func):
    @pytest.mark.skipif(
        not elastic_is_running_locally(), reason="Elastic is not running locally"
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
