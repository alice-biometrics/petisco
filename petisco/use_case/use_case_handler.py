from typing import List, Any

from meiga import Result
from meiga.decorators import meiga

from petisco.logger.interface_logger import ERROR, INFO
from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger
from petisco.use_case.use_case import UseCase


class _UseCaseHandler:
    def __init__(
        self,
        logger=NotImplementedLogger(),
        logging_parameters_whitelist: List[str] = None,
        logging_types_blacklist: List[Any] = None,
    ):
        self.logger = logger
        self.logging_parameters_whitelist = logging_parameters_whitelist
        self.logging_types_blacklist = logging_types_blacklist

    def __call__(self, cls):
        if not issubclass(cls, UseCase):
            raise TypeError("@use_case_handler only decorates UseCase subclasses")

        class UseCaseWrapped(cls):
            logger = self.logger
            logging_parameters_whitelist = self.logging_parameters_whitelist
            logging_types_blacklist = self.logging_types_blacklist

            def execute(self, *args, **kwargs):
                correlation_id = kwargs.get("correlation_id")

                log_message = LogMessage(
                    layer="use_case",
                    operation=f"{cls.__name__}",
                    correlation_id=correlation_id,
                )

                log_message.message = f"Start"
                self.logger.log(INFO, log_message.to_json())

                if self.logging_parameters_whitelist:
                    loggable_kwargs = [
                        (k, v)
                        for k, v in kwargs.items()
                        if k in self.logging_parameters_whitelist
                    ]

                    if loggable_kwargs:
                        log_message.message = dict(loggable_kwargs)
                        self.logger.log(INFO, log_message.to_json())

                result = self._run_execute(*args, **kwargs)

                if not isinstance(result, Result):
                    return result

                detail = getattr(result.value, "message", None)
                if detail:
                    detail = f"-> {detail}"
                else:
                    detail = ""

                if result.is_failure:
                    log_message.message = f"{result} {detail}"
                    self.logger.log(ERROR, log_message.to_json())
                else:
                    if not self._is_logging_type(result.value):
                        log_message.message = (
                            f"Success result of type: {type(result.value).__name__}"
                        )
                    else:
                        log_message.message = f"{result.value}"
                    self.logger.log(INFO, log_message.to_json())

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

        return UseCaseWrapped


use_case_handler = _UseCaseHandler
