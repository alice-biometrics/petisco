import os
from functools import wraps
from inspect import signature
from typing import Any, Callable, Dict, List, Type, Union

import elasticapm
from loguru import logger
from meiga import Error, Failure, Result

from petisco.base.application.middleware.middleware import Middleware
from petisco.base.application.middleware.notifier_middleware import NotifierMiddleware
from petisco.base.application.middleware.print_middleware import PrintMiddleware
from petisco.base.application.middleware.request_responded_middleware import (
    RequestRespondedMiddleware,
)
from petisco.base.domain.errors.critical_error import CriticalError
from petisco.base.domain.errors.unknown_error import UnknownError
from petisco.base.misc.result_mapper import ResultMapper
from petisco.extra.meiga import WaitingForEarlyReturn


def get_middleware_instances(config: Dict[str, Any]) -> List[Middleware]:
    middlewares_instances: List[Middleware] = []

    middlewares_configs = getattr(config, "middlewares", [])
    if not middlewares_configs:
        middlewares_configs = get_middlewares_configuration_from_environment()

    for middlewares_config in middlewares_configs:
        if not isinstance(middlewares_config, Middleware):
            middlewares_instances.append(middlewares_config())
        else:
            middlewares_instances.append(middlewares_config)

    return middlewares_instances


def get_middlewares_configuration_from_environment():
    def gettype(name: str) -> Type[Middleware]:
        lookup_table = {
            "NotifierMiddleware": NotifierMiddleware,
            "RequestRespondedMiddleware": RequestRespondedMiddleware,
            "PrintMiddleware": PrintMiddleware,
        }
        my_type = lookup_table.get(name)
        if not my_type:
            raise TypeError(
                f"Value {name} in PETISCO_DEFAULT_MIDDLEWARES is not valid. Please, use {list(lookup_table.keys())}"
            )
        return my_type

    default_middlewares_names: Union[str, None] = os.getenv(
        "PETISCO_DEFAULT_MIDDLEWARES"
    )
    if not default_middlewares_names:
        return []
    default_middlewares_names_list = default_middlewares_names.split(",")
    return [
        gettype(middleware_name) for middleware_name in default_middlewares_names_list
    ]


def wrapper(
    execute_func: Callable[..., Any],
    wrapped_class_name: str,
    config: Any,
    mapper: ResultMapper,
) -> Callable[..., Any]:
    @wraps(execute_func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        middlewares = get_middleware_instances(config)
        arguments = signature(execute_func).bind(*args, **kwargs).arguments
        arguments.pop("self")

        for middleware in middlewares:
            try:
                middleware.set_data(wrapped_class_name, arguments)
                middleware.before()
            except Exception as exception:
                logger.error(f"Error in the {wrapped_class_name} middlewares (before).")
                logger.exception(exception)

        try:
            result = execute_func(*args, **kwargs)
        except WaitingForEarlyReturn as exc:
            result = exc.result
        except Error as error:
            result = Failure(error)
        except Exception as exception:
            unknown_error = UnknownError.from_exception(
                exception=exception,
                arguments=arguments if len(arguments) > 0 else args,
                class_name=wrapped_class_name,
            )
            result = Failure(unknown_error)
            client = elasticapm.get_client()
            if client:
                client.capture_exception()

        if not isinstance(result, Result):
            raise TypeError(
                f"Controller Error: Return value `{result}` ({type(result)}) must be a `meiga.Result`"
            )

        if isinstance(result.value, CriticalError) and len(arguments) > 0:
            formatted_args = {
                k: str(v) if type(v) is not bytes else "bytes"
                for k, v in arguments.items()
            }
            result.value.set_additional_info(formatted_args)

        result.set_transformer(mapper.map)
        for middleware in middlewares:
            if result:
                try:
                    middleware.after(result)
                except Exception as exception:
                    logger.error(
                        f"Error in the {wrapped_class_name} middlewares (after)."
                    )
                    logger.exception(exception)

        return result

    return wrapped
