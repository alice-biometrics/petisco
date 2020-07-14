import requests
from meiga import Result, Error, Failure, Success
from requests.exceptions import MissingSchema, ConnectionError, Timeout

from petisco.http.request_errors import (
    MissingSchemaRequestError,
    TimeoutRequestError,
    ConnectionRequestError,
    UnknownRequestError,
)
from petisco.http.response import Response


class Request:
    @staticmethod
    def __is_binary_content(content_type):
        binary_types = ["binary", "video", "image", "multipart/form-data"]
        if any(binary_type in content_type for binary_type in binary_types):
            return True
        return False

    @staticmethod
    def get(
        url: str, binary_info: dict = None, string_info: dict = None, headers=None
    ) -> Result[Response, Error]:
        return Request.execute(url, "GET", binary_info, string_info, headers)

    @staticmethod
    def post(
        url: str, binary_info: dict = None, string_info: dict = None, headers=None
    ) -> Result[Response, Error]:
        return Request.execute(url, "POST", binary_info, string_info, headers)

    @staticmethod
    def delete(
        url: str, binary_info: dict = None, string_info: dict = None, headers=None
    ) -> Result[Response, Error]:
        return Request.execute(url, "DELETE", binary_info, string_info, headers)

    @staticmethod
    def execute(
        url: str,
        request: str = "POST",
        binary_info: dict = None,
        string_info: dict = None,
        headers=None,
    ) -> Result[Response, Error]:
        response = None
        try:
            if request == "GET":
                response = requests.get(
                    url=url,
                    files=binary_info,
                    data=string_info,
                    headers=headers,
                    timeout=(5, 25),
                )
            elif request == "POST":
                response = requests.post(
                    url=url,
                    files=binary_info,
                    data=string_info,
                    headers=headers,
                    timeout=(5, 25),
                )
            elif request == "DELETE":
                response = requests.delete(url=url, headers=headers, timeout=(5, 25))
        except MissingSchema:
            return Failure(MissingSchemaRequestError())
        except Timeout:
            return Failure(TimeoutRequestError())
        except ConnectionError:
            return Failure(ConnectionRequestError())
        except Exception as e:
            return Failure(UnknownRequestError(error_message=e))

        if isinstance(response, requests.models.Response):
            if Request.__is_binary_content(response.headers.get("Content-Type", [])):
                return Success(
                    Response(
                        status_code=response.status_code,
                        content=response.content,
                        headers=response.headers,
                    )
                )
            try:
                json_response = response.json()
            except ValueError:
                json_response = response.text
            return Success(
                Response(
                    status_code=response.status_code,
                    content=json_response,
                    headers=response.headers,
                )
            )
        else:
            return Failure(UnknownRequestError())
