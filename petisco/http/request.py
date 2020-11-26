import requests
from meiga import Result, Error, Failure, Success
from requests.exceptions import MissingSchema, ConnectionError, Timeout

from petisco.domain.timedelta_parser import TimeDeltaParser
from petisco.http.request_errors import (
    MissingSchemaRequestError,
    TimeoutRequestError,
    ConnectionRequestError,
    UnknownRequestError,
    UnauthorizedRequestError,
    BadRequestError,
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
        url: str,
        binary_info: dict = None,
        string_info: dict = None,
        json_info: dict = None,
        headers=None,
        auth=None,
    ) -> Result[Response, Error]:
        return Request.execute(
            url, "GET", binary_info, string_info, json_info, headers, auth
        )

    @staticmethod
    def post(
        url: str,
        binary_info: dict = None,
        string_info: dict = None,
        json_info: dict = None,
        headers=None,
        auth=None,
    ) -> Result[Response, Error]:
        return Request.execute(
            url, "POST", binary_info, string_info, json_info, headers, auth
        )

    @staticmethod
    def patch(
        url: str,
        binary_info: dict = None,
        string_info: dict = None,
        json_info: dict = None,
        headers=None,
        auth=None,
    ) -> Result[Response, Error]:
        return Request.execute(
            url, "PATCH", binary_info, string_info, json_info, headers, auth
        )

    @staticmethod
    def delete(
        url: str,
        binary_info: dict = None,
        string_info: dict = None,
        json_info: dict = None,
        headers=None,
        auth=None,
    ) -> Result[Response, Error]:
        return Request.execute(
            url, "DELETE", binary_info, string_info, json_info, headers, auth
        )

    @staticmethod
    def execute(
        url: str,
        request: str = "POST",
        binary_info: dict = None,
        string_info: dict = None,
        json_info: dict = None,
        headers=None,
        auth=None,
    ) -> Result[Response, Error]:
        response = None
        try:
            if request == "GET":
                response = requests.get(
                    url=url,
                    params=string_info,
                    headers=headers,
                    timeout=(5, 25),
                    auth=auth,
                )
            elif request == "POST":
                response = requests.post(
                    url=url,
                    files=binary_info,
                    data=string_info,
                    json=json_info,
                    headers=headers,
                    timeout=(5, 25),
                    auth=auth,
                )
            elif request == "PATCH":
                response = requests.patch(
                    url=url,
                    data=string_info,
                    json=json_info,
                    headers=headers,
                    timeout=(5, 25),
                    auth=auth,
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
            return Failure(UnknownRequestError.from_exception(e))

        if response.status_code == 400:
            return Failure(BadRequestError.from_response(response))

        if response.status_code == 401:
            return Failure(UnauthorizedRequestError.from_response(response))

        if response.status_code < 200 or response.status_code > 299:
            return Failure(UnknownRequestError.from_response(response))

        if isinstance(response, requests.models.Response):
            if Request.__is_binary_content(response.headers.get("Content-Type", [])):
                return Success(
                    Response(
                        status_code=response.status_code,
                        content=response.content,
                        headers=response.headers,
                        completed_in_ms=TimeDeltaParser.ms_from_timedelta(
                            response.elapsed
                        ),
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
                    completed_in_ms=TimeDeltaParser.ms_from_timedelta(response.elapsed),
                )
            )
        else:
            return Failure(UnknownRequestError.from_response(response))
