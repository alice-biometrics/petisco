import os
from functools import wraps
from inspect import signature

import elasticapm
from meiga import Error, Failure
from meiga.on_failure_exception import OnFailureException

from petisco.base.application.middleware.notifier_middleware import NotifierMiddleware
from petisco.base.application.middleware.print_middleware import PrintMiddleware
from petisco.base.domain.errors.unknown_error import UnknownError


def get_middleware_classes(config):
    def gettype(name):
        lookup_table = {
            "NotifierMiddleware": NotifierMiddleware,
            "PrintMiddleware": PrintMiddleware,
        }
        my_type = lookup_table.get(name)
        if not my_type:
            raise TypeError(
                f"Value {name} in PETISCO_DEFAULT_MIDDLEWARES is not valid. Please, use {list(lookup_table.keys())}"
            )
        return my_type

    middlewares_classes = getattr(config, "middlewares", [])
    if not middlewares_classes:
        default_middlewares_names = os.getenv("PETISCO_DEFAULT_MIDDLEWARES", [])
        if default_middlewares_names:
            default_middlewares_names = default_middlewares_names.split(",")
            middlewares_classes = [
                gettype(middleware_name)
                for middleware_name in default_middlewares_names
            ]

    return middlewares_classes


def wrapper(execute_func, wrapped_class_name, config, mapper):
    @wraps(execute_func)
    def wrapped(*args, **kwargs):
        middleware_classes = get_middleware_classes(config)
        arguments = signature(execute_func).bind(*args, **kwargs).arguments
        arguments.pop("self")
        middlewares = [
            klass(wrapped_class_name, arguments) for klass in middleware_classes
        ]

        for middleware in middlewares:
            middleware.before()

        try:
            result = execute_func(*args, **kwargs)
        except OnFailureException as exc:
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

        for middleware in middlewares:
            if result:
                middleware.after(result)

        mapped_result = mapper.map(result)

        return mapped_result

    return wrapped
