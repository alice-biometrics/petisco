from fastapi import HTTPException


def assert_http_exception(
    http_exception_current: HTTPException, http_exception_expected: HTTPException
):
    assert (
        http_exception_current.status_code == http_exception_expected.status_code
        and http_exception_current.detail == http_exception_expected.detail
    ), f"| status_code: {http_exception_current.status_code} - {http_exception_expected.status_code} | -> | detail: {http_exception_current.detail} - {http_exception_expected.detail}|"
