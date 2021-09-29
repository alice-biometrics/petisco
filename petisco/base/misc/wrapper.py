from functools import wraps
from inspect import signature

from meiga import Error, Failure
from meiga.on_failure_exception import OnFailureException

from petisco.base.domain.errors.unknown_error import UnknownError


def wrapper(execute_func, wrapped_class_name, config, mapper):
    @wraps(execute_func)
    def wrapped(*args, **kwargs):
        middlewares_classes = getattr(config, "middlewares", [])

        arguments = signature(execute_func).bind(*args, **kwargs).arguments
        arguments.pop("self")
        middlewares = [
            klass(wrapped_class_name, arguments) for klass in middlewares_classes
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

        mapped_result = mapper.map(result)
        for middleware in middlewares:
            if result:
                middleware.after(result)
        return mapped_result

    return wrapped
