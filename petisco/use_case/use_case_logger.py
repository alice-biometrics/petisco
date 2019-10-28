from typing import List

import logging
from meiga import Result
from meiga.decorators import meiga

from petisco.logger.log_message import LogMessage
from petisco.use_case.use_case import UseCase


class UseCaseLogger(object):
    def __init__(self, logger=None, logging_parameters_whitelist: List[str] = None):
        self.logger = logger
        self.logging_parameters_whitelist = logging_parameters_whitelist

    def __call__(self, cls):
        if not issubclass(cls, UseCase):
            raise TypeError("UseCaseLogger only decorates UseCase subclasses")

        class UseCaseWrapped(cls):
            logger = self.logger
            logging_parameters_whitelist = self.logging_parameters_whitelist

            def execute(self, *args, **kwargs):
                correlation_id = kwargs.get("correlation_id")

                log_message = LogMessage(
                    layer="use_case",
                    operation=f"{cls.__name__}",
                    correlation_id=correlation_id,
                )

                log_message.message = f"Start"
                self.logger.log(
                    logging.INFO, log_message.to_json()
                )

                if self.logging_parameters_whitelist:
                    loggable_kwargs = [
                        (k, v)
                        for k, v in kwargs.items()
                        if k in self.logging_parameters_whitelist
                    ]

                    if loggable_kwargs:
                        log_message.message = dict(loggable_kwargs)
                        self.logger.log(
                            logging.INFO, log_message.to_json()
                        )

                result = self._run_execute(*args, **kwargs)

                if not isinstance(result, Result):
                    return result

                detail = getattr(result.value, "message", None)
                if detail:
                    detail = f"-> {detail}"
                else:
                    detail = ""

                if result.is_failure:
                    log_message.message = f"Error: {result} {detail}"
                    self.logger.log(
                        logging.ERROR, log_message.to_json()
                    )
                else:
                    log_message.message = f"Result: {result.value}"
                    self.logger.log(
                        logging.INFO, log_message.to_json()
                    )

                return result

            @meiga
            def _run_execute(self, *args, **kwargs) -> Result:
                return super().execute(*args, **kwargs)

        return UseCaseWrapped


use_case_logger = UseCaseLogger
