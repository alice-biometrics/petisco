import json
import time
import random

from petisco.logger.interface_logger import INFO
from petisco.events.event import Event
from functools import wraps
from meiga import Result
from meiga.decorators import meiga

from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger


class _SubscriberHandler:
    def __init__(
        self,
        logger=NotImplementedLogger(),
        message_broker: str = "rabbitmq",
        filter_routing_key: str = None,
        delay_after: float = 0,
        percentage_simulate_rejection: float = None,
    ):
        """
        Parameters
        ----------
        logger
            A ILogger implementation. Default NotImplementedLogger
        message_broker:
            Select Message Brokent. For now, only available rabbitmq
        filter_routing_key:
            Only process, if received message is equal to given filter_routing_key
        delay_after:
            Delay ack or reject for a given number of seconds.
        percentage_simulate_rejection:
            Percentage of simulate rejection when the result is a success. [0.0 -> 1.0]. Where 1.0 rejects all the events.

        """
        self.logger = logger
        if message_broker != "rabbitmq":
            raise TypeError(
                f"Petisco Subscriber: message broker {message_broker} is not implemented. Try with rabbitmq"
            )
        self.filter_routing_key = filter_routing_key
        self.delay_after = delay_after
        self.percentage_simulate_rejection = percentage_simulate_rejection

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            @meiga
            def run_controller(*args, **kwargs) -> Result:
                return func(*args, **kwargs)

            ch, method, properties, body = args

            log_message = LogMessage(layer="subscriber", operation=f"{func.__name__}")
            log_message.message = json.dumps(
                {"routing_key": method.routing_key, "body": json.loads(body)}
            )
            self.logger.log(INFO, log_message.to_json())

            if (
                self.filter_routing_key
                and self.filter_routing_key != method.routing_key
            ):
                return

            try:
                event = Event.from_json(body)
            except TypeError:
                event = Event.from_deprecated_json(body)
            except:  # noqa E722
                return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

            result = run_controller(event)

            if self.delay_after:
                time.sleep(self.delay_after)

            if result is None:
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            else:
                if result.is_success:
                    if (
                        self.percentage_simulate_rejection
                        and random.random() < self.percentage_simulate_rejection
                    ):
                        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
                    else:
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

        return wrapper


subscriber_handler = _SubscriberHandler
