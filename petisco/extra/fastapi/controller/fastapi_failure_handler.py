from typing import Dict

from fastapi import HTTPException
from meiga import Result

from petisco.base.application.controller.http_error import DEFAULT_HTTP_ERROR_MESSAGE
from petisco.legacy.controller.errors.http_error import HttpError
from petisco.legacy.controller.errors.internal_http_error import InternalHttpError


def fastapi_failure_handler(result: Result, error_map: Dict[type, HttpError]):
    domain_error = result.value
    error_type = type(domain_error)
    http_error = error_map.get(error_type, InternalHttpError())
    detail = (
        http_error.message
        if http_error.message != DEFAULT_HTTP_ERROR_MESSAGE
        else domain_error.detail()
    )
    raise HTTPException(status_code=http_error.code, detail=detail)
