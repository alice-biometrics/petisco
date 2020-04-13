import inspect
import traceback

from functools import wraps
from typing import Callable, Tuple, Dict, List, Any
from meiga import Result, Error, Success
from meiga.decorators import meiga
from petisco.application.petisco import Petisco
from petisco.controller.errors.internal_http_error import InternalHttpError
from petisco.controller.errors.known_result_failure_handler import (
    KnownResultFailureHandler,
)

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.events.request_responded import RequestResponded
from petisco.events.event_config import EventConfig
from petisco.frameworks.flask.flask_headers_provider import flask_headers_provider
from petisco.logger.interface_logger import ERROR, INFO
from petisco.controller.errors.http_error import HttpError
from petisco.security.token_manager.not_implemented_token_manager import (
    NotImplementedTokenManager,
)
from petisco.security.token_manager.token_manager import TokenManager
from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger
from petisco.tools.timer import timer

DEFAULT_SUCCESS_MESSAGE = {"message": "OK"}, 200
DEFAULT_ERROR_MESSAGE = HttpError().handle()


class _ControllerHandler:
    def __init__(
        self,
        app_name: str = "app-undefined",
        app_version: str = None,
        logger=NotImplementedLogger(),
        event_config: EventConfig = EventConfig(),
        token_manager: TokenManager = NotImplementedTokenManager(),
        success_handler: Callable[[Result], Tuple[Dict, int]] = None,
        error_handler: Callable[[Result], HttpError] = None,
        headers_provider: Callable = flask_headers_provider,
        logging_types_blacklist: List[Any] = [bytes],
        petisco: Petisco = None,
    ):
        """
        Parameters
        ----------
        app_name
            Application Name
        app_version
            Application Version
        logger
            A ILogger implementation. Default NotImplementedLogger
        event_config
            EventConfig object. Here, you can define event management.
        token_manager
            TokenManager object. Here, you can define how to deal with JWT Tokens
        success_handler
            Handler to deal with Success Results
        error_handler
            Handler to deal with Failure Results
        headers_provider
            Injectable function to provide headers. By default is used headers_provider
        logging_types_blacklist
            Logging Blacklist. Object of defined Type will not be logged. By default ( [bytes] ) bytes object won't be logged.
        petisco
            Use Petisco to set params as: app_name, app_version, logger, or event_manager (EventConfig)
        """
        self.app_name = app_name
        self.app_version = app_version
        self.logger = logger
        self.event_config = event_config
        self.token_manager = token_manager
        self.success_handler = success_handler
        self.error_handler = error_handler
        self.headers_provider = headers_provider
        self.logging_types_blacklist = logging_types_blacklist
        self.petisco = petisco
        self.set_petisco_dependencies()

    def set_petisco_dependencies(self):
        if self.petisco:
            self.app_name = self.petisco.app_name
            self.app_version = self.petisco.app_version
            self.logger = self.petisco.logger
            if self.event_config.is_configured:
                self.event_config.event_manager = self.petisco.event_manager_provider()

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            @timer
            @meiga
            def run_controller(*args, **kwargs) -> Result:
                params = inspect.getfullargspec(func).args
                kwargs = {k: v for k, v in kwargs.items() if k in params}
                return func(*args, **kwargs)

            info_id = None
            is_success = False
            elapsed_time = None
            try:
                kwargs = add_petisco(kwargs)
                kwargs = add_headers(kwargs)
                result_kwargs = add_info_id(kwargs)

                log_message = LogMessage(
                    layer="controller", operation=f"{func.__name__}"
                )
                if result_kwargs.is_failure:
                    http_response = self.handle_failure(log_message, result_kwargs)
                else:
                    kwargs, info_id = result_kwargs.value
                    log_message.info_id = info_id
                    log_message.message = "Start"
                    self.logger.log(INFO, log_message.to_json())

                    result_controller, elapsed_time = run_controller(*args, **kwargs)

                    if result_controller.is_failure:
                        http_response = self.handle_failure(
                            log_message, result_controller
                        )
                    else:
                        if isinstance(
                            result_controller.value, tuple(self.logging_types_blacklist)
                        ):
                            log_message.message = f"Success result of type: {type(result_controller.value).__name__}"
                        else:
                            log_message.message = f"{result_controller}"
                        self.logger.log(INFO, log_message.to_json())
                        http_response = (
                            self.success_handler(result_controller)
                            if self.success_handler
                            else DEFAULT_SUCCESS_MESSAGE
                        )
                        is_success = True
            except Exception as e:
                log_message = LogMessage(
                    layer="controller",
                    operation=f"{func.__name__}",
                    message=f"Error {func.__name__}: {repr(e.__class__)} {e} | {traceback.format_exc()}",
                )
                self.logger.log(ERROR, log_message.to_json())
                http_response = InternalHttpError().handle()

            request_responded = RequestResponded(
                app_name=self.app_name,
                app_version=self.app_version,
                controller=f"{func.__name__}",
                is_success=is_success,
                http_response=http_response,
                elapsed_time=elapsed_time,
                additional_info=self.event_config.get_additional_info(kwargs),
            )
            self.event_config.event_manager.publish(
                topic=self.event_config.event_topic,
                event=request_responded,
                info_id=info_id,
            )

            return http_response

        def add_headers(kwargs):
            headers = self.headers_provider()
            kwargs = dict(kwargs, headers=headers)
            return kwargs

        def add_petisco(kwargs):
            kwargs = dict(kwargs, petisco=self.petisco)
            return kwargs

        @meiga
        def add_info_id(kwargs) -> Result[Tuple[str, InfoId], Error]:
            headers = kwargs.get("headers", {})

            info_id = self.token_manager.execute(headers).unwrap_or_return()

            kwargs = dict(kwargs, info_id=info_id)
            return Success((kwargs, info_id))

        return wrapper

    def handle_failure(
        self, log_message: LogMessage, result: Result
    ) -> Tuple[dict, int]:
        log_message.message = f"{result}"
        self.logger.log(ERROR, log_message.to_json())
        known_result_failure_handler = KnownResultFailureHandler(result)
        http_response = DEFAULT_ERROR_MESSAGE
        if not known_result_failure_handler.is_a_result_known_error:
            if self.error_handler:
                http_error = self.error_handler(result)

                if not issubclass(http_error.__class__, HttpError):
                    raise TypeError(
                        "Returned object from error_handler must be subclasses of HttpError"
                    )

                http_response = http_error.handle()
        else:
            http_response = known_result_failure_handler.http_error.handle()
        return http_response


controller_handler = _ControllerHandler
