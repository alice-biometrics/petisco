import json
from typing import Any, Dict, Union

from loguru import logger
from meiga import Result

from petisco.base.application.controller.http_error import HttpError
from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.message.domain_event import DomainEvent

REQUEST_RESPONDED_UNWRAP_ERROR = (
    {
        "error": {
            "type": "RequestRespondedUnwrapError",
            "message": "Cannot unwrap http response from decorated function",
        }
    },
)


class RequestResponded(DomainEvent):
    app_name: str
    app_version: str
    controller: str
    is_success: bool
    http_response: Dict[str, Any]
    elapsed_time: float

    @staticmethod
    def create(
        app_name: str,
        app_version: str,
        controller: str,
        is_success: bool,
        http_response: Dict[str, Any],
        elapsed_time: float,
    ) -> "RequestResponded":
        app_name = app_name
        app_version = app_version
        controller = controller
        is_success = is_success
        elapsed_time = elapsed_time
        http_response = RequestResponded.set_http_response(is_success, http_response)

        return RequestResponded(
            app_name=app_name,
            app_version=app_version,
            controller=controller,
            is_success=is_success,
            elapsed_time=elapsed_time,
            http_response=http_response,
        )

    @staticmethod
    def _get_content(response: Union[Any, str]) -> Dict[str, Any]:
        content = {"message": str(response)}

        if isinstance(response, dict):
            content = {"message": json.dumps(response)}
        elif isinstance(response, HttpError):
            content = {"message": response.detail}
        elif isinstance(response, Result):
            if isinstance(response.value, DomainError):
                content = {
                    "message": response.value.detail(),
                }
            else:
                content = {"message": str(response.value)}
        content["message"] = content["message"][:300]
        return content

    @staticmethod
    def set_http_response(is_success: bool, http_response: Any) -> Dict[str, Any]:
        try:
            _http_response = {
                "content": REQUEST_RESPONDED_UNWRAP_ERROR,
                "status_code": 500,
            }

            if is_success:
                _http_response["content"] = {"message": "OK"}
                _http_response["status_code"] = 200
            elif isinstance(http_response, HttpError):
                _http_response["content"] = RequestResponded._get_content(http_response)
                _http_response["status_code"] = http_response.status_code
            else:
                _http_response["content"] = RequestResponded._get_content(http_response)
                _http_response["status_code"] = 500
        except Exception as e:
            logger.error(e)
            raise e
        return _http_response
