import os
import string
import random

import pytest

from petisco import RabbitMqConnector
from petisco.event.configurer.infrastructure.rabbitmq_event_configurer import (
    RabbitMqEventConfigurer,
)


@pytest.fixture
def given_any_organization() -> str:
    return f"acme"


@pytest.fixture
def given_any_service() -> str:
    return f"petisco"


@pytest.fixture
def given_rabbitmq_connector():
    return RabbitMqConnector()


@pytest.fixture
def given_rabbitmq_configurer(
    given_rabbitmq_connector, given_any_organization, given_any_service
):
    configurer = RabbitMqEventConfigurer(
        given_rabbitmq_connector, given_any_organization, given_any_service
    )
    yield configurer
    configurer.clear()


@pytest.fixture
def given_any_topic():
    return "topic"


@pytest.fixture
def given_random_str() -> str:
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(5)).lower()


@pytest.fixture
def given_random_organization(given_random_str) -> str:
    return f"acme-{given_random_str}"


@pytest.fixture
def given_random_service(given_random_str) -> str:
    return f"service-{given_random_str}"


@pytest.fixture
def given_random_topic(given_random_str) -> str:
    return f"topic-{given_random_str}"


@pytest.fixture
def given_a_short_message_ttl():
    original_value = os.environ.get("RABBITMQ_MESSAGE_TTL")

    os.environ["RABBITMQ_MESSAGE_TTL"] = "10"

    yield

    if original_value:
        os.environ["RABBITMQ_MESSAGE_TTL"] = original_value
