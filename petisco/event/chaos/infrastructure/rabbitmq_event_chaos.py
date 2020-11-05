import os
import random
from time import sleep
from typing import Optional, Dict, List

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from petisco.event.chaos.domain.interface_event_chaos import IEventChaos

EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK_KEY = "EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK"
EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS_KEY = (
    "EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS"
)
EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES_KEY = (
    "EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES"
)

EVENT_CHAOS_PROTECTED_ROUTING_KEYS_KEY = "EVENT_CHAOS_PROTECTED_ROUTING_KEYS"


class RabbitMqEventChaos(IEventChaos):
    def __init__(
        self,
        percentage_simulate_nack: Optional[float] = None,
        delay_before_even_handler_second: Optional[float] = None,
        percentage_simulate_failures: Optional[float] = None,
        protected_routing_keys: Optional[List[str]] = None,
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
        protected_routing_keys
            Routing keys where chaos will not be applied
        """
        self._set_percentage_simulate_nack(percentage_simulate_nack)
        self._set_delay_before_even_handler_second(delay_before_even_handler_second)
        self._set_percentage_simulate_failures(percentage_simulate_failures)
        self._set_protected_routing_keys(protected_routing_keys)

    def _set_percentage_simulate_nack(self, percentage_simulate_nack):
        if percentage_simulate_nack is None:
            percentage_simulate_nack = os.environ.get(
                EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK_KEY
            )
        self.percentage_simulate_nack = self._float(percentage_simulate_nack)

    def _set_delay_before_even_handler_second(self, delay_before_even_handler_second):
        if delay_before_even_handler_second is None:
            delay_before_even_handler_second = os.environ.get(
                EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS_KEY
            )
        self.delay_before_even_handler_second = self._float(
            delay_before_even_handler_second
        )

    def _set_percentage_simulate_failures(self, percentage_simulate_failures):
        if percentage_simulate_failures is None:
            percentage_simulate_failures = os.environ.get(
                EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES_KEY
            )
        self.percentage_simulate_failures = self._float(percentage_simulate_failures)

    def _set_protected_routing_keys(self, protected_routing_keys):
        if protected_routing_keys is None:
            protected_routing_keys = os.environ.get(
                EVENT_CHAOS_PROTECTED_ROUTING_KEYS_KEY
            )
        self.protected_routing_keys = self._list(protected_routing_keys)

    def _float(self, value):
        return float(value) if value is not None else None

    def _list(self, value):
        if value is None:
            return None

        if isinstance(value, str):
            value = list(value.split(","))
        return value

    def __repr__(self):
        return f"RabbitMqEventChaos: {self.info()}"

    def info(self) -> Dict:
        return {
            EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK_KEY: self.percentage_simulate_nack,
            EVENT_CHAOS_DELAY_BEFORE_EVENT_HANDLER_SECONDS_KEY: self.delay_before_even_handler_second,
            EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES_KEY: self.percentage_simulate_failures,
            EVENT_CHAOS_PROTECTED_ROUTING_KEYS_KEY: self.protected_routing_keys,
        }

    def nack_simulation(self, ch: BlockingChannel, method: Basic.Deliver) -> bool:
        routing_key = method.routing_key if method else None

        if (self.percentage_simulate_nack is None) or (
            random.random() > self.percentage_simulate_nack
        ):
            return False

        if (
            self.protected_routing_keys is None
            or routing_key not in self.protected_routing_keys
        ):
            ch.basic_nack(delivery_tag=method.delivery_tag)
            return True
        else:
            return False

    def failure_simulation(self, method: Basic.Deliver) -> bool:
        routing_key = method.routing_key if method else None

        if (self.percentage_simulate_failures is None) or (
            random.random() > self.percentage_simulate_failures
        ):
            return False
        else:
            return (
                True
                if self.protected_routing_keys is None
                or routing_key not in self.protected_routing_keys
                else False
            )

    def delay(self):
        if self.delay_before_even_handler_second is None:
            pass
        else:
            sleep(self.delay_before_even_handler_second)
