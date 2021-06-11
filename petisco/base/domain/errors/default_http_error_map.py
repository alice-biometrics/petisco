from petisco.base.application.controller.http_error import HttpError
from petisco.base.domain.errors.defaults.already_exists import (
    AlreadyExists,
    ClientAlreadyExists,
    UserAlreadyExists,
)
from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid
from petisco.base.domain.errors.defaults.not_found import (
    NotFound,
    ClientNotFound,
    UserNotFound,
)

DEFAULT_HTTP_ERROR_MAP = {
    NotFound: HttpError(status_code=404),
    AlreadyExists: HttpError(status_code=409),
    ClientNotFound: HttpError(status_code=404),
    ClientAlreadyExists: HttpError(status_code=409),
    UserNotFound: HttpError(status_code=404),
    UserAlreadyExists: HttpError(status_code=409),
    InvalidUuid: HttpError(status_code=422),
}
