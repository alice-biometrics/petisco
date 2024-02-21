from functools import wraps
from inspect import signature
from typing import Any, Callable

import elasticapm
from loguru import logger
from meiga import Error, Failure

from petisco.base.domain.errors.unknown_error import UnknownError
from petisco.base.domain.value_objects.operation_type import OperationType
from petisco.base.misc.result_mapper import ResultMapper
from petisco.base.misc.wrapper import get_middleware_instances
from petisco.extra.meiga import WaitingForEarlyReturn


def async_wrapper(
    execute_func: Callable[..., Any],
    wrapped_class_name: str,
    config: Any,
    mapper: ResultMapper,
) -> Callable[..., Any]:
    @wraps(execute_func)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        from petisco import Controller, MessageSubscriber

        middlewares = get_middleware_instances(config)
        arguments = signature(execute_func).bind(*args, **kwargs).arguments
        arguments.pop("self")

        for middleware in middlewares:
            if (
                middleware.operation_affected == OperationType.ALL
                or middleware.operation_affected == OperationType.CONTROLLER
                and issubclass(args[0].__class__, Controller)
                or middleware.operation_affected == OperationType.SUBSCRIBER
                and issubclass(args[0].__class__, MessageSubscriber)
            ):
                pass
            else:
                continue

            try:
                middleware.set_data(wrapped_class_name, arguments)
                middleware.before()
            except Exception as exception:
                logger.error(f"Error in the {wrapped_class_name} middlewares (before).")
                logger.exception(exception)

        try:
            result = await execute_func(*args, **kwargs)
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

        try:
            result.set_transformer(mapper.map)
        except AttributeError:  # noqa
            raise TypeError(
                f"Controller Error: Return value `{result}` ({type(result)}) must be a `meiga.Result` to "
                f"transform values to success and failure handlers."
            )

        for middleware in middlewares:
            if (
                middleware.operation_affected == OperationType.ALL
                or middleware.operation_affected == OperationType.CONTROLLER
                and issubclass(args[0].__class__, Controller)
                or middleware.operation_affected == OperationType.SUBSCRIBER
                and issubclass(args[0].__class__, MessageSubscriber)
            ):
                pass
            else:
                continue

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
