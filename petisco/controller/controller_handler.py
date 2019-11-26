import inspect
from functools import wraps
import traceback
from typing import Callable, Tuple, Dict, List, Any

from meiga import Result
from meiga.decorators import meiga

from petisco.controller.errors.bad_request_http_error import BadRequestHttpError
from petisco.controller.errors.known_result_failure_handler import (
    KnownResultFailureHandler,
)
from petisco.controller.tokens.jwt_decorator import jwt
from petisco.logger.interface_logger import ERROR, INFO
from petisco.controller.errors.http_error import HttpError
from petisco.controller.tokens.jwt_config import JwtConfig
from petisco.frameworks.flask.correlation_id_provider import (
    flask_correlation_id_provider,
)
from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger

DEFAULT_SUCCESS_MESSAGE = {"message": "OK"}, 200
DEFAULT_ERROR_MESSAGE = HttpError().handle()


class _ControllerHandler:
    def __init__(
        self,
        logger=NotImplementedLogger(),
        jwt_config: JwtConfig = None,
        success_handler: Callable[[Result], Tuple[Dict, int]] = None,
        error_handler: Callable[[Result], HttpError] = None,
        correlation_id_provider: Callable = flask_correlation_id_provider,
        logging_types_blacklist: List[Any] = [bytes],
    ):
        self.logger = logger
        self.jwt_config = jwt_config
        self.success_handler = success_handler
        self.error_handler = error_handler
        self.correlation_id_provider = correlation_id_provider
        self.logging_types_blacklist = logging_types_blacklist

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            @meiga
            @jwt(jwt_config=self.jwt_config)
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
                self.logger.log(INFO, log_message.to_json())
                result = run_controller(*args, **kwargs)
                if result.is_success:
                    if isinstance(result.value, tuple(self.logging_types_blacklist)):
                        log_message.message = (
                            f"Success result of type: {type(result.value).__name__}"
                        )
                    else:
                        log_message.message = f"{result}"
                    self.logger.log(INFO, log_message.to_json())
                    return (
                        self.success_handler(result)
                        if self.success_handler
                        else DEFAULT_SUCCESS_MESSAGE
                    )
                else:
                    log_message.message = f"{result}"
                    self.logger.log(ERROR, log_message.to_json())
                    known_result_failure_handler = KnownResultFailureHandler(result)

                    if not known_result_failure_handler.is_a_result_known_error:
                        if not self.error_handler:
                            return DEFAULT_ERROR_MESSAGE

                        http_error = self.error_handler(result)

                        if not issubclass(http_error.__class__, HttpError):
                            raise TypeError(
                                "Returned object from error_handler must be subclasses of HttpError"
                            )

                        return http_error.handle()
                    else:
                        return known_result_failure_handler.http_error.handle()

            except Exception as e:
                log_message.message = (
                    f"Error {func.__name__}: {e} | {traceback.print_exc()}"
                )
                self.logger.log(ERROR, log_message.to_json())
                return BadRequestHttpError(suffix=traceback.print_exc()).handle()

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


controller_handler = _ControllerHandler
