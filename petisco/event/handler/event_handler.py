import inspect

import traceback

from petisco.application.petisco import Petisco
from petisco.domain.errors.critical_error import CriticalError
from petisco.logger.interface_logger import DEBUG
from petisco.event.shared.domain.event import Event
from functools import wraps
from meiga import Result, Failure
from meiga.decorators import meiga

from petisco.logger.log_message import LogMessage
from petisco.notifier.domain.notifier_exception_message import NotifierExceptionMessage
from petisco.notifier.infrastructure.not_implemented_notifier import (
    NotImplementedNotifier,
)

DEFAULT_LOGGER = None
DEFAULT_NOTIFIER = None


class _EventHandler:
    def __init__(self, logger=DEFAULT_LOGGER, notifier=DEFAULT_NOTIFIER):
        """
        Parameters
        ----------
        logger
            A ILogger implementation. Default NotImplementedLogger
        notifier
            A INotifier implementation. If not specified it will get it from Petisco.get_notifier(). You can also use NotImplementedNotifier
        """
        self.logger = logger
        self.notifier = notifier
        self._check_logger()
        self._check_notifier()

    def _check_logger(self):
        if self.logger == DEFAULT_LOGGER:
            from petisco import Petisco

            self.logger = Petisco.get_logger()

    def _check_notifier(self):
        if self.notifier == DEFAULT_NOTIFIER:
            self.notifier = NotImplementedNotifier()

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            @meiga
            def run_event_handler(*args, **kwargs) -> Result:
                return func(*args, **kwargs)

            self._check_logger()
            self._check_notifier()

            event: Event = args[0]

            log_message = LogMessage(
                layer="event_handler", operation=f"{func.__name__}"
            )

            self.logger.log(
                DEBUG,
                log_message.set_message(
                    {"event": event.event_name, "body": event.to_json()}
                ),
            )

            try:
                result = run_event_handler(*args, **kwargs)
            except Exception as exception:
                result = Failure(
                    CriticalError(
                        exception=exception,
                        input_parameters=kwargs if len(kwargs) > 0 else args,
                        executor=f"{func.__name__} (Event Handler)",
                        traceback=traceback.format_exc(),
                    )
                )

            self.logger.log(DEBUG, log_message.set_message({"result": result}))

            self.notify(result)

            return result

        wrapper.__signature__ = inspect.signature(func)
        return wrapper

    @meiga
    def notify(self, result):
        if result is not None and result.is_failure:
            error = result.value
            if issubclass(error.__class__, CriticalError):
                self.notifier.publish(
                    NotifierExceptionMessage(
                        exception=error.exception,
                        executor=error.executor,
                        input_parameters=error.input_parameters,
                        traceback=error.traceback,
                        info_petisco=Petisco.get_info(),
                    )
                )


event_handler = _EventHandler
