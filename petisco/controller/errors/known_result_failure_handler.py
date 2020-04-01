from meiga import Result

from petisco.controller.errors.http_error import HttpError
from petisco.controller.errors.invalid_token_http_error import InvalidTokenHttpError
from petisco.security.token_decoder.invalid_token_error import InvalidTokenError


class KnownResultFailureHandler:
    def __init__(self, result: Result):
        self.domain_error = result.value

        self.http_error = HttpError()
        self.is_a_result_known_error = False
        domain_error = result.value

        if isinstance(domain_error, InvalidTokenError):
            self.http_error = InvalidTokenHttpError(suffix=domain_error.message)
            self.is_a_result_known_error = True
