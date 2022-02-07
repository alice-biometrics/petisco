from typing import Dict

import elasticapm
from fastapi import HTTPException
from loguru import logger
from meiga import Result

from petisco import DEFAULT_HTTP_ERROR_MAP
from petisco.base.application.controller.http_error import (
    DEFAULT_HTTP_ERROR_DETAIL,
    HttpError,
)
from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.errors.unknown_error import UnknownError


def fastapi_failure_handler(result: Result, error_map: Dict[type, HttpError]):
    domain_error = result.value
    error_type = type(domain_error)
    http_error = error_map.get(error_type, HttpError())

    elasticapm.set_custom_context({"http_response": str(http_error)})

    internal_error_message = None
    if isinstance(result.value, UnknownError):
        internal_error_message = str(result.value.__dict__)
    elif error_type not in error_map:
        internal_error_message = (
            f"Error '{result.value.__class__.__name__}' is not mapped in controller"
        )

    if internal_error_message is not None:
        logger.error(internal_error_message)
        elasticapm.set_custom_context(
            {"internal_error_message": internal_error_message}
        )

    detail = "Unknown Error"
    if isinstance(domain_error, DomainError):
        detail = (
            http_error.detail
            if http_error.detail != DEFAULT_HTTP_ERROR_DETAIL
            else domain_error.detail()
        )
    http_exception = HTTPException(
        status_code=http_error.status_code, detail=detail, headers=http_error.headers
    )

    if (
        isinstance(domain_error, DomainError)
        and type(domain_error) not in DEFAULT_HTTP_ERROR_MAP.keys()
    ):
        logger.error(f"DomainError:  {domain_error.__repr__()}")
        logger.error(f"HTTPException: {http_exception.__repr__()}")

    raise http_exception
