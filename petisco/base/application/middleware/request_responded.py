import json
from json import JSONDecodeError
from typing import Any, Dict, Union

from loguru import logger
from meiga import Result

from petisco import DomainError, DomainEvent, HttpError

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
    info_id: Union[str, None] = None

    @staticmethod
    def create(
        app_name: str,
        app_version: str,
        controller: str,
        is_success: bool,
        http_response: Dict[str, Any],
        elapsed_time: float,
        info_id: Union[str, None] = None,
    ) -> "RequestResponded":
        app_name = app_name
        app_version = app_version
        controller = controller
        is_success = is_success
        elapsed_time = elapsed_time
        http_response = RequestResponded.set_http_response(is_success, http_response)
        info_id = info_id

        return RequestResponded(
            app_name=app_name,
            app_version=app_version,
            controller=controller,
            is_success=is_success,
            elapsed_time=elapsed_time,
            http_response=http_response,
            info_id=info_id,
        )

    @staticmethod
    def _get_content(
        is_success: bool, response: Union[Dict[str, Any], str]
    ) -> Dict[str, Any]:
        content = response
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except JSONDecodeError:
                pass
            except Exception as e:
                logger.error(e)
                raise e
        content_size = len(str(content))

        if content_size > 300:
            if is_success:
                content = {
                    "message": f"Response OK (Trimmed message: {content[:300]})",
                    "message_size": content_size,
                }
            else:
                error_type = "Error"
                if isinstance(content, dict):
                    error_type = content.get("error", {}).get("type", "Error")
                content = {
                    "error_type": error_type,
                    "message": f"Response Error (Trimmed message: {content.value[:300]})",
                    "message_size": content_size,
                }
        else:
            if isinstance(content, dict):
                content = {"message": json.dumps(content), "message_size": content_size}
            elif isinstance(content, HttpError):
                content = {"message": content.detail, "message_size": content_size}
            elif isinstance(content, Result):
                if isinstance(content.value, DomainError):
                    content = {
                        "message": content.value.detail(),
                        "message_size": content_size,
                    }
                else:
                    content = {"message": content.value, "message_size": content_size}
            else:
                content = {"message": content, "message_size": content_size}
        return content

    @staticmethod
    def set_http_response(is_success: bool, http_response: Any) -> Dict[str, Any]:
        try:
            _http_response = {
                "content": REQUEST_RESPONDED_UNWRAP_ERROR,
                "status_code": 500,
            }
            if is_success:
                if isinstance(http_response, Result):
                    _http_response["content"] = RequestResponded._get_content(
                        is_success, http_response.value
                    )
                else:
                    _http_response["content"] = RequestResponded._get_content(
                        is_success, http_response
                    )
                _http_response["status_code"] = 200
            else:
                if isinstance(http_response, HttpError):
                    _http_response["content"] = RequestResponded._get_content(
                        is_success, http_response.detail
                    )
                    _http_response["status_code"] = http_response.status_code
                else:
                    _http_response["content"] = RequestResponded._get_content(
                        is_success, http_response
                    )
                    _http_response["status_code"] = 500
        except Exception as e:
            logger.error(e)
            raise e
        return _http_response
