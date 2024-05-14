from typing import NoReturn

from fastapi import HTTPException
from loguru import logger
from meiga import AnyResult

from petisco import DEFAULT_HTTP_ERROR_MAP
from petisco.base.application.controller.error_map import ErrorMap
from petisco.base.application.controller.http_error import (
    DEFAULT_HTTP_ERROR_DETAIL,
    HttpError,
)
from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.errors.unknown_error import UnknownError
from petisco.extra.elastic_apm.is_elastic_apm_available import is_elastic_apm_available


def fastapi_failure_handler(result: AnyResult, error_map: ErrorMap) -> NoReturn:
    domain_error = result.value
    error_type = type(domain_error)
    http_error = error_map.get(error_type, HttpError())

    if is_elastic_apm_available():
        import elasticapm  # noqa

        elasticapm.set_custom_context({"http_response": str(http_error)})

    internal_error_message = None
    if isinstance(result.value, UnknownError):
        internal_error_message = str(result.value.__dict__)
    elif error_type not in error_map:
        internal_error_message = f"Error '{result.value.__class__.__name__}' is not mapped in controller"

    if internal_error_message is not None:
        logger.error(internal_error_message)
        if is_elastic_apm_available():
            import elasticapm  # noqa

            elasticapm.set_custom_context({"internal_error_message": internal_error_message})

    detail = http_error.detail
    if isinstance(domain_error, DomainError):
        detail = (
            http_error.detail if http_error.detail != DEFAULT_HTTP_ERROR_DETAIL else domain_error.detail()
        )
    else:
        logger.warning(
            f"fastapi_failure_handler: {domain_error.__class__.__name__} is not a DomainError (warning "
            f"mapping error)"
        )

    assert isinstance(http_error.status_code, int)
    http_exception = HTTPException(
        status_code=http_error.status_code, detail=detail, headers=http_error.headers
    )

    if isinstance(domain_error, DomainError) and type(domain_error) not in DEFAULT_HTTP_ERROR_MAP:
        logger.error(f"DomainError:  {domain_error.__repr__()}")
        logger.error(f"HTTPException: {http_exception.__repr__()}")

    raise http_exception
