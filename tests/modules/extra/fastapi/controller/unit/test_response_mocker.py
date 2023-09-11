from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.responses import JSONResponse

from petisco.extra.fastapi import ResponseMocker


@pytest.mark.unit
class TestResponseMocker:
    def should_work_without_header(self):
        request = Mock(Request)
        request.headers = Headers(headers={})
        dependency = ResponseMocker()
        response = dependency(request=request)
        assert response is None

    def should_return_json_response_when_mocked_value_is_200(self):
        request = Mock(Request)
        request.headers = Headers(headers={"X-Status-Code-Mock-Response": "200"})
        dependency = ResponseMocker()
        response = dependency(request=request)
        assert isinstance(response, JSONResponse)

    @pytest.mark.parametrize("status_code", [300, 400, 500])
    def should_raise_http_exception_when_mocked_value_is_an_error(self, status_code):
        request = Mock(Request)
        request.headers = Headers(
            headers={"X-Status-Code-Mock-Response": str(status_code)}
        )
        dependency = ResponseMocker()

        with pytest.raises(HTTPException) as exc_info:
            dependency(request=request)

        exception = exc_info.value
        assert exception.status_code == status_code

    def should_raise_http_exception_with_mapped_responses(self):
        request = Mock(Request)
        request.headers = Headers(headers={"X-Status-Code-Mock-Response": "400"})
        dependency = ResponseMocker(responses={400: {"detail": "my_detail"}})

        with pytest.raises(HTTPException) as exc_info:
            dependency(request=request)

        exception = exc_info.value
        assert exception.status_code == 400
        assert exception.detail == {"detail": "my_detail"}

    def should_return_json_response_when_modify_header_key_and_mocked_value_is_200(
        self,
    ):
        other_header_key = "X-MY-STATUS-CODE"
        request = Mock(Request)
        request.headers = Headers(headers={other_header_key: "200"})
        dependency = ResponseMocker(header_key=other_header_key)
        response = dependency(request=request)
        assert isinstance(response, JSONResponse)
