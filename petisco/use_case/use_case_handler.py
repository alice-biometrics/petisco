from typing import List, Any

from meiga import Result
from meiga.decorators import meiga

from petisco.logger.interface_logger import ERROR, INFO, DEBUG
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
                info_id = kwargs.get("info_id")

                log_message = LogMessage(
                    layer="use_case", operation=f"{cls.__name__}", info_id=info_id
                )

                self.logger.log(INFO, log_message.set_message(f"Running Use Case"))

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

                result = self._run_execute(*args, **kwargs)

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

        return UseCaseWrapped


use_case_handler = _UseCaseHandler
