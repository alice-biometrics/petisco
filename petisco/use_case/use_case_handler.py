import traceback
from typing import List, Any

from meiga import Result, Failure
from meiga.decorators import meiga

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.errors.critical_error import CriticalError
from petisco.domain.errors.unknown_error import UnknownError
from petisco.logger.interface_logger import ERROR, DEBUG
from petisco.logger.log_message import LogMessage
from petisco.notifier.domain.notifier_exception_message import NotifierExceptionMessage
from petisco.use_case.use_case import UseCase
from petisco.application.petisco import Petisco

DEFAULT_LOGGER = None
DEFAULT_NOTIFIER = None


class _UseCaseHandler:
    def __init__(
        self,
        logger=DEFAULT_LOGGER,
        logging_parameters_whitelist: List[str] = None,
        logging_types_blacklist: List[Any] = None,
        notifier=DEFAULT_NOTIFIER,
    ):
        self.logger = logger
        self.logging_parameters_whitelist = logging_parameters_whitelist
        self.logging_types_blacklist = logging_types_blacklist
        self.notifier = notifier
        self._check_logger()
        self._check_notifier()

    def _check_logger(self):
        if self.logger == DEFAULT_LOGGER:
            self.logger = Petisco.get_logger()

    def _check_notifier(self):
        if self.notifier == DEFAULT_NOTIFIER:
            self.notifier = Petisco.get_notifier()

    def __call__(self, cls):
        if not issubclass(cls, UseCase):
            raise TypeError("@use_case_handler only decorates UseCase subclasses")

        class UseCaseWrapped(cls):
            logger = self.logger
            logging_parameters_whitelist = self.logging_parameters_whitelist
            logging_types_blacklist = self.logging_types_blacklist
            notifier = self.notifier

            def execute(self, *args, **kwargs):
                info_id = kwargs.get("info_id")

                log_message = LogMessage(
                    layer="use_case", operation=f"{cls.__name__}", info_id=info_id
                )

                self.logger.log(DEBUG, log_message.set_message(f"Running Use Case"))

                if self.logging_parameters_whitelist:
                    loggable_kwargs = {}
                    for key, value in kwargs.items():
                        if key not in self.logging_parameters_whitelist:
                            continue
                        if getattr(value, "to_json", None):
                            loggable_kwargs[key] = value.to_json()
                        else:
                            loggable_kwargs[key] = value

                    if loggable_kwargs:
                        self.logger.log(DEBUG, log_message.set_message(loggable_kwargs))

                try:
                    result = self._run_execute(*args, **kwargs)
                except Exception as exception:
                    result = Failure(
                        UnknownError(
                            exception=exception,
                            input_parameters=kwargs if len(kwargs) > 0 else args,
                            executor=f"{cls.__name__} (Use Case)",
                            traceback=traceback.format_exc(),
                            filter_parameters=["headers"],
                        )
                    )

                if not isinstance(result, Result):
                    return result

                detail = getattr(result.value, "message", None)
                if detail:
                    detail = f"-> {detail}"
                else:
                    detail = ""

                if result.is_failure:
                    self.logger.log(
                        ERROR, log_message.set_message(f"{result} {detail}")
                    )
                    self.notify(result, info_id)
                else:
                    if not self._is_logging_type(result.value):
                        message = (
                            f"Success result of type: {type(result.value).__name__}"
                        )
                    else:
                        message = f"{result.value}"
                    self.logger.log(DEBUG, log_message.set_message(message))

                return result

            def _is_logging_type(self, value):
                if self.logging_types_blacklist:
                    for logging_type in self.logging_types_blacklist:
                        if isinstance(value, logging_type):
                            return False
                return True

            @meiga
            def _run_execute(self, *args, **kwargs) -> Result:
                return super().execute(*args, **kwargs)

            @meiga
            def notify(self, result, info_id: InfoId = None):
                if result.is_failure:
                    error = result.value
                    if issubclass(error.__class__, CriticalError):
                        self.notifier.publish(
                            NotifierExceptionMessage(
                                exception=error.exception,
                                executor=error.executor,
                                input_parameters=error.input_parameters,
                                traceback=error.traceback,
                                info_id=info_id,
                                info_petisco=Petisco.get_info(),
                            )
                        )

        return UseCaseWrapped


use_case_handler = _UseCaseHandler
