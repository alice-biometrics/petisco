from typing import Dict

from meiga import Result, Error

from petisco.application.petisco import Petisco
from petisco.controller.controller_handler import controller_handler
from petisco.controller.errors.http_error import HttpError
from petisco.modules.healthcheck.domain.persistence_error import PersistenceError
from petisco.modules.healthcheck.application.healthcheck_provider import (
    HealthcheckProvider,
)


class PersistenceHttpError(HttpError):
    def __init__(
        self,
        message: str = "Cannot connect with configured persistence. If you are not using persistence, just delete it from petisco.yml",
        code: int = 503,
    ):
        self.message = message
        self.code = code
        super(PersistenceHttpError, self).__init__(message, code)


def error_handler(result: Result) -> HttpError:
    domain_error = result.value
    http_error = HttpError()
    if isinstance(domain_error, PersistenceError):
        http_error = PersistenceHttpError()
    return http_error


@controller_handler(
    success_handler=lambda result: (result.value, 200), error_handler=error_handler
)
def healthcheck() -> Result[Dict, Error]:
    return HealthcheckProvider().execute(Petisco.get_instance())
