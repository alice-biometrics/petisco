from typing import Any
from unittest.mock import Mock

import pytest
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco import RabbitMqEventChaos


@pytest.mark.integration
def test_should_configure_with_envvars(monkeypatch):
    monkeypatch.setenv("EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK", "1.0")
    monkeypatch.setenv("EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS", "1.0")
    monkeypatch.setenv("EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES", "1.0")
    monkeypatch.setenv(
        "EVENT_CHAOS_PROTECTED_ROUTING_KEYS", "dead_letter.store,dl-legacy"
    )

    chaos = RabbitMqEventChaos()

    assert chaos.info() == {
        "EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK": 1.0,
        "EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS": 1.0,
        "EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES": 1.0,
        "EVENT_CHAOS_PROTECTED_ROUTING_KEYS": ["dead_letter.store", "dl-legacy"],
    }


@pytest.mark.integration
def test_should_create_default_rabbitmq_event_chaos():
    chaos = RabbitMqEventChaos()

    assert chaos.nack_simulation(None, None) is False
    chaos.delay()
    assert chaos.failure_simulation(None) is False


@pytest.mark.integration
def test_should_create_default_rabbitmq_event_chaos_with_env_percentage_simulate_nack_1(
    monkeypatch
):
    monkeypatch.setenv("EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK", "1.0")

    chaos = RabbitMqEventChaos()

    mock_channel = Mock(BlockingChannel)
    mock_method = Mock(Basic.Deliver)
    mock_method.delivery_tag = Mock(Any)
    mock_method.routing_key = Mock(Any)

    assert chaos.nack_simulation(mock_channel, mock_method) is True
    chaos.delay()
    assert chaos.failure_simulation(mock_method) is False

    mock_channel.basic_nack.assert_called_once()


@pytest.mark.integration
def test_should_create_default_rabbitmq_event_chaos_with_env_percentage_simulate_failures_1(
    monkeypatch
):
    monkeypatch.setenv("EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES", "1.0")
    monkeypatch.setenv("EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS", "0.2")

    chaos = RabbitMqEventChaos()
    assert chaos.nack_simulation(None, None) is False
    chaos.delay()
    assert chaos.failure_simulation(None) is True


@pytest.mark.integration
def test_should_create_rabbitmq_event_chaos_with_percentage_simulate_nack_1():
    chaos = RabbitMqEventChaos(percentage_simulate_nack=1.0)

    mock_channel = Mock(BlockingChannel)
    mock_method = Mock(Basic.Deliver)
    mock_method.delivery_tag = Mock(Any)
    mock_method.routing_key = Mock(Any)

    assert chaos.nack_simulation(mock_channel, mock_method) is True
    chaos.delay()
    assert chaos.failure_simulation(mock_method) is False

    mock_channel.basic_nack.assert_called_once()


@pytest.mark.integration
def test_should_create_rabbitmq_event_chaos_with_percentage_simulate_nack_but_with_protected_routing_key():
    chaos = RabbitMqEventChaos(
        percentage_simulate_nack=1.0, protected_routing_keys=["routing_key"]
    )

    mock_channel = Mock(BlockingChannel)
    mock_method = Mock(Basic.Deliver)
    mock_method.delivery_tag = Mock(Any)
    mock_method.routing_key = "routing_key"

    assert chaos.nack_simulation(mock_channel, mock_method) is False
    chaos.delay()
    assert chaos.failure_simulation(mock_method) is False


@pytest.mark.integration
def test_should_create_rabbitmq_event_chaos_with_percentage_simulate_failure_but_with_protected_routing_key():
    chaos = RabbitMqEventChaos(
        percentage_simulate_failures=1.0, protected_routing_keys=["routing_key"]
    )

    mock_channel = Mock(BlockingChannel)
    mock_method = Mock(Basic.Deliver)
    mock_method.routing_key = "routing_key"

    assert chaos.nack_simulation(mock_channel, mock_method) is False
    chaos.delay()
    assert chaos.failure_simulation(mock_method) is False


@pytest.mark.integration
def test_should_create_rabbitmq_event_chaos_with_percentage_simulate_failure_and_nck_but_with_protected_routing_key():
    chaos = RabbitMqEventChaos(
        percentage_simulate_nack=1.0,
        percentage_simulate_failures=1.0,
        protected_routing_keys=["routing_key"],
    )

    mock_channel = Mock(BlockingChannel)
    mock_method = Mock(Basic.Deliver)
    mock_method.delivery_tag = Mock(Any)
    mock_method.routing_key = "routing_key"

    assert chaos.nack_simulation(mock_channel, mock_method) is False
    chaos.delay()
    assert chaos.failure_simulation(mock_method) is False


@pytest.mark.integration
def test_should_create_rabbitmq_event_chaos_with_percentage_simulate_failures_1():
    chaos = RabbitMqEventChaos(percentage_simulate_failures=1.0)

    mock_method = Mock(Basic.Deliver)
    mock_method.routing_key = Mock(Any)

    assert chaos.nack_simulation(None, None) is False
    chaos.delay()
    assert chaos.failure_simulation(mock_method) is True
