import inspect
import logging
from functools import wraps
import traceback
from typing import Callable

from meiga import Result

from petisco.controller.correlation_id import CorrelationId
from petisco.controller.errors.http_error import HttpError
from petisco.controller.jwt.jwt_config import JwtConfig
from petisco.frameworks.flask.correlation_id_provider import flask_correlation_id_provider
from petisco.logger.log_message import LogMessage

DEFAULT_SUCCESS_MESSAGE = {"message": "OK"}, 200
DEFAULT_ERROR_MESSAGE = HttpError().handle()


class ControllerDecorator(object):
    def __init__(
        self,
        logger=None,
        jwt_config: JwtConfig = None,
        success_handler: Callable = None,
        error_handler: Callable = None,
        correlation_id_provider: Callable = flask_correlation_id_provider
    ):
        self.logger = logger
        self.jwt_config = jwt_config
        self.success_handler = success_handler
        self.error_handler = error_handler
        self.correlation_id_provider = correlation_id_provider

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_message = LogMessage(layer="controller", operation=f"{func.__name__}")

            # @jwt(jwt_config=self.jwt_config)
            def run_controller(*args, **kwargs) -> Result:
                return func(*args, **kwargs)

            correlation_id, kwargs = update_correlation_id(kwargs)
            log_message = LogMessage(
                layer="controller",
                operation=f"{func.__name__}",
                correlation_id=correlation_id,
            )

            try:
                log_message.message = "Start"
                self.logger.log(logging.INFO, log_message.to_json())
                result = run_controller(*args, **kwargs)
                log_message.message = f"Result: {result}"
                self.logger.log(logging.INFO, log_message.to_json())
                if result.is_success:
                    return (
                        self.success_handler(result)
                        if self.success_handler
                        else DEFAULT_SUCCESS_MESSAGE
                    )
                else:
                    return (
                        self.error_handler(result)
                        if self.error_handler
                        else DEFAULT_ERROR_MESSAGE
                    )

            except Exception as e:
                log_message.message = (
                    f"Error {func.__name__}: {e} | {traceback.print_exc()}"
                )
                self.logger.log(logging.ERROR, log_message.to_json())

        def update_correlation_id(kwargs):
            signature = inspect.signature(func)
            if (
                "correlation_id" in signature.parameters
                and "correlation_id" not in kwargs
            ):
                correlation_id = self.correlation_id_provider(func.__name__)
                kwargs = dict(kwargs, correlation_id=correlation_id)
            else:
                correlation_id = None
            return correlation_id, kwargs

        return wrapper


controller = ControllerDecorator
