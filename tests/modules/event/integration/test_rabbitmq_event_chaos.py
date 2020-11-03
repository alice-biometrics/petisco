from typing import Any
from unittest.mock import Mock

import pytest
from meiga import isSuccess, Failure
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco import RabbitMqEventChaos
from petisco.event.chaos.domain.event_chaos_error import EventChaosError


@pytest.mark.integration
def test_should_create_default_rabbitmq_event_chaos():
    chaos = RabbitMqEventChaos()

    assert chaos.nack_simulation(None, None) is False
    chaos.delay()
    assert chaos.simulate_failure_on_result(isSuccess) == isSuccess


@pytest.mark.integration
def test_should_create_rabbitmq_event_chaos_with_percentage_simulate_nack_1():
    chaos = RabbitMqEventChaos(percentage_simulate_nack=1.0)

    mock_channel = Mock(BlockingChannel)
    mock_method = Mock(Basic.Deliver)
    mock_method.delivery_tag = Mock(Any)

    assert chaos.nack_simulation(mock_channel, mock_method) is True
    chaos.delay()
    assert chaos.simulate_failure_on_result(isSuccess) == isSuccess

    mock_channel.basic_nack.assert_called_once()


@pytest.mark.integration
def test_should_create_rabbitmq_event_chaos_with_percentage_simulate_failures_1():
    chaos = RabbitMqEventChaos(percentage_simulate_failures=1.0)

    assert chaos.nack_simulation(None, None) is False
    chaos.delay()
    assert chaos.simulate_failure_on_result(isSuccess) == Failure(
        EventChaosError(Exception())
    )
