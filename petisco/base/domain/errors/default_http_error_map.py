from petisco.legacy.controller.errors.http_error import HttpError
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
    NotFound: HttpError(code=404),
    AlreadyExists: HttpError(code=409),
    ClientNotFound: HttpError(code=404),
    ClientAlreadyExists: HttpError(code=409),
    UserNotFound: HttpError(code=404),
    UserAlreadyExists: HttpError(code=409),
    InvalidUuid: HttpError(code=422),
}
