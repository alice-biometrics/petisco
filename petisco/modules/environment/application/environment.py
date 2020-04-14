from typing import Dict

from meiga import Result, Error

from petisco.application.petisco import Petisco
from petisco.controller.controller_handler import controller_handler
from petisco.controller.errors.http_error import HttpError
from petisco.modules.environment.application.environment_provider import (
    EnvironmentProvider,
)
from petisco.modules.environment.domain.environment_provider_error import (
    EnvironmentProviderError,
)


class EnvironmentProviderHttpError(HttpError):
    def __init__(
        self,
        message: str = "Unknown error gathering environment information",
        code: int = 500,
    ):
        self.message = message
        self.code = code
        super(EnvironmentProviderHttpError, self).__init__(message, code)


def error_handler(result: Result) -> HttpError:
    domain_error = result.value
    http_error = HttpError()
    if isinstance(domain_error, EnvironmentProviderError):
        http_error = EnvironmentProviderHttpError()
    return http_error


@controller_handler(
    success_handler=lambda result: (result.value, 200), error_handler=error_handler
)
def environment() -> Result[Dict, Error]:
    return EnvironmentProvider().execute(Petisco.get_instance())
