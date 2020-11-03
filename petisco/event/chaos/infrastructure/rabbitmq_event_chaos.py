import os
import random
from time import sleep
from typing import Optional, Dict

from meiga import Failure, Result
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco.event.chaos.domain.event_chaos_error import EventChaosError
from petisco.event.chaos.domain.interface_event_chaos import IEventChaos

EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK_KEY = "EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK"
EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS_KEY = (
    "EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS"
)
EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES_KEY = (
    "EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES"
)


class RabbitMqEventChaos(IEventChaos):
    def __init__(
        self,
        percentage_simulate_nack: Optional[float] = os.environ.get(
            EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK_KEY
        ),
        delay_before_even_handler_second: Optional[float] = os.environ.get(
            EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS_KEY
        ),
        percentage_simulate_failures: Optional[float] = os.environ.get(
            EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES_KEY
        ),
    ):
        """
        Parameters
        ----------
        percentage_simulate_nack
            Percentage of simulate nack [0.0 -> 1.0]. Where 1.0 rejects all the event.
        delay_before_even_handler_second
            Delay event handler execution for a given number of seconds.
        percentage_simulate_failures
            Percentage of simulate failures [0.0 -> 1.0]. Where 1.0 simulate always a failure on handlers.
        """
        self.percentage_simulate_nack = percentage_simulate_nack
        self.delay_before_even_handler_second = delay_before_even_handler_second
        self.percentage_simulate_failures = percentage_simulate_failures

    def info(self) -> Dict:
        return {
            EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK_KEY: self.percentage_simulate_nack,
            EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS_KEY: self.delay_before_even_handler_second,
            EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES_KEY: self.percentage_simulate_failures,
        }

    def nack_simulation(self, ch: BlockingChannel, method: Basic.Deliver):
        if (self.percentage_simulate_nack is None) or (
            random.random() > self.percentage_simulate_nack
        ):
            return False
        ch.basic_nack(delivery_tag=method.delivery_tag)
        return True

    def simulate_failure_on_result(self, result: Result) -> Result:
        if (self.percentage_simulate_failures is None) or (
            random.random() > self.percentage_simulate_failures
        ):
            return result
        else:
            return Failure(EventChaosError(Exception()))

    def delay(self):
        if self.delay_before_even_handler_second is None:
            pass
        else:
            sleep(self.delay_before_even_handler_second)
