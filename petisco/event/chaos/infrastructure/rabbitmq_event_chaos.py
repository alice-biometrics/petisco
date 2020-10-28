import os
import random
from time import sleep
from typing import Optional

from meiga import Failure, Result
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco.event.chaos.domain.event_chaos_error import EventChaosError
from petisco.event.chaos.domain.interface_event_chaos import IEventChaos


class RabbitMqEventChaos(IEventChaos):
    def __init__(
        self,
        percentage_simulate_nack: Optional[float] = os.environ.get(
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK"
        ),
        delay_after_result: Optional[float] = os.environ.get(
            "EVENT_CHAOS_DELAY_AFTER_OPERATION_SECONDS"
        ),
        percentage_simulate_failures: Optional[float] = os.environ.get(
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES"
        ),
    ):
        """
        Parameters
        ----------
        percentage_simulate_nack
            Percentage of simulate nack [0.0 -> 1.0]. Where 1.0 rejects all the event.
        delay_after_result
            Delay response for a given number of seconds.
        percentage_simulate_failures
            Percentage of simulate failures [0.0 -> 1.0]. Where 1.0 simulate always a failure on handlers.
        """
        self.percentage_simulate_nack = percentage_simulate_nack
        self.delay_after_result = delay_after_result
        self.percentage_simulate_failures = percentage_simulate_failures

    def info(self):
        return {
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK": self.percentage_simulate_nack,
            "EVENT_CHAOS_DELAY_AFTER_OPERATION_SECONDS": self.delay_after_result,
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES": self.percentage_simulate_failures,
        }

    def nack_simulation(self, ch: BlockingChannel, method: Basic.Deliver):
        if (self.percentage_simulate_nack is None) or (
            random.random() > self.percentage_simulate_nack
        ):
            return
        ch.basic_nack(delivery_tag=method.delivery_tag)

    def simulate_failure_on_result(self, result: Result) -> Result:
        if (self.percentage_simulate_nack is None) or (
            random.random() > self.percentage_simulate_failures
        ):
            return result
        else:
            return Failure(EventChaosError(Exception()))

    def delay(self):
        if self.delay_after_result is None:
            pass
        else:
            sleep(self.delay_after_result)
