import pytest

from petisco import HttpError
from petisco.base.application.controller.http_error import DEFAULT_HTTP_ERROR_DETAIL


@pytest.mark.unit
def test_http_error_should_success_when_construct():
    http_error = HttpError()

    assert http_error.status_code == 500
    assert http_error.detail == DEFAULT_HTTP_ERROR_DETAIL
    assert http_error.type_error == "HttpError"


@pytest.mark.unit
def test_http_error_should_success_when_construct_a_inherit_http_error_with_status_code():
    class MyHttpError(HttpError):
        status_code = 422

    http_error = MyHttpError()

    assert http_error.status_code == 422
    assert http_error.detail == DEFAULT_HTTP_ERROR_DETAIL
    assert http_error.type_error == "MyHttpError"


@pytest.mark.unit
def test_http_error_should_success_when_construct_a_inherit_http_error_with_status_code_and_detail():
    class MyHttpError(HttpError):
        status_code = 422
        detail = "my-message"

    http_error = MyHttpError()

    assert http_error.status_code == 422
    assert http_error.detail == "my-message"
    assert http_error.type_error == "MyHttpError"


@pytest.mark.unit
def test_http_error_should_success_when_construct_a_inherit_http_error_with_status_code_detail_and_type_error():
    class MyHttpError(HttpError):
        status_code = 422
        detail = "my-message"
        type_error = "my-error"

    http_error = MyHttpError()

    assert http_error.status_code == 422
    assert http_error.detail == "my-message"
    assert http_error.type_error == "my-error"
