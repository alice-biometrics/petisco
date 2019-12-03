from functools import wraps
import traceback

from meiga import Result, isFailure
from meiga.decorators import meiga

from petisco.events.event import Event
from petisco.logger.interface_logger import ERROR, INFO
from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger


class _CommandHandler:
    def __init__(self, logger=NotImplementedLogger()):
        self.logger = logger

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            @meiga
            def run_command(*args, **kwargs) -> Result:
                return func(*args, **kwargs)

            event = kwargs.get("event")
            if not event or not issubclass(event.__class__, Event):
                raise TypeError(
                    "@command_handler only decorates function with at least one event as input"
                )

            log_message = LogMessage(
                layer="command",
                operation=f"{func.__name__}",
                correlation_id=event.correlation_id,
            )

            try:
                log_message.message = f"Event received: {event}"
                self.logger.log(INFO, log_message.to_json())
                result = run_command(*args, **kwargs)
                if result.is_success:
                    log_message.message = f"{result}"
                    self.logger.log(INFO, log_message.to_json())
                else:
                    log_message.message = f"{result}"
                    self.logger.log(ERROR, log_message.to_json())
                return result

            except Exception as e:
                log_message.message = f"Error {func.__name__}: {repr(e.__class__)} {e} | {traceback.format_exc()}"
                self.logger.log(ERROR, log_message.to_json())
                return isFailure

        return wrapper


command_handler = _CommandHandler
