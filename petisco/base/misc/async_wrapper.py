from functools import wraps
from inspect import signature
from typing import Any, Callable

import elasticapm
from meiga import Error, Failure
from meiga.on_failure_exception import OnFailureException

from petisco.base.domain.errors.unknown_error import UnknownError
from petisco.base.misc.result_mapper import ResultMapper
from petisco.base.misc.wrapper import get_middleware_instances


def async_wrapper(
    execute_func: Callable[..., Any],
    wrapped_class_name: str,
    config: Any,
    mapper: ResultMapper,
) -> Callable[..., Any]:
    @wraps(execute_func)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        middlewares = get_middleware_instances(config)
        arguments = signature(execute_func).bind(*args, **kwargs).arguments
        arguments.pop("self")

        for middleware in middlewares:
            middleware.set_data(wrapped_class_name, arguments)
            middleware.before()

        try:
            result = await execute_func(*args, **kwargs)
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