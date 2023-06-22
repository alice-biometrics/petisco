from typing import Any, Dict, Optional

import pytest

from petisco import HttpError
from petisco.base.application.controller.http_error import DEFAULT_HTTP_ERROR_DETAIL


@pytest.mark.unit
class TestHttpError:
    def should_success_when_construct_default(self):  # noqa
        http_error = HttpError()

        assert http_error.status_code == 500
        assert http_error.detail == DEFAULT_HTTP_ERROR_DETAIL
        assert http_error.type_error == "HttpError"

    def should_success_when_construct_a_inherit_http_error_with_status_code(
        self,
    ):  # noqa
        class MyHttpError(HttpError):
            status_code: int = 422

        http_error = MyHttpError()

        assert http_error.status_code == 422
        assert http_error.detail == DEFAULT_HTTP_ERROR_DETAIL
        assert http_error.type_error == "MyHttpError"

    def should_success_when_construct_a_inherit_http_error_with_status_code_and_detail(
        self,
    ):  # noqa
        class MyHttpError(HttpError):
            status_code: int = 422
            detail: str = "my-message"

        http_error = MyHttpError()

        assert http_error.status_code == 422
        assert http_error.detail == "my-message"
        assert http_error.type_error == "MyHttpError"

    def should_success_when_construct_a_inherit_http_error_with_status_code_detail_and_type_error(
        self,
    ):  # noqa
        class MyHttpError(HttpError):
            status_code: int = 422
            detail: str = "my-message"
            type_error: str = "my-error"

        http_error = MyHttpError()

        assert http_error.status_code == 422
        assert http_error.detail == "my-message"
        assert http_error.type_error == "my-error"

    def should_success_when_construct_with_headers(self):  # noqa
        class MyHttpError(HttpError):
            status_code: int = 401
            detail: str = "Unauthorized"
            headers: Optional[Dict[str, Any]] = {"WWW-Authenticate": 'authType="OTP"'}

        http_error = MyHttpError()

        assert http_error.status_code == 401
        assert http_error.detail == "Unauthorized"
        assert http_error.headers == {"WWW-Authenticate": 'authType="OTP"'}
