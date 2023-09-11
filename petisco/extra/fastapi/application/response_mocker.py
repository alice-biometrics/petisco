from typing import Any, Dict, Union

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


class ResponseMocker:
    """
    This class mocks the router response if the client sends a valid response value through request headers
    """

    def __init__(
        self,
        header_key: str = "X-Status-Code-Mock-Response",
        responses: Union[Dict[Union[int, str], Dict[str, Any]], None] = None,
    ) -> None:
        self.header_key = header_key
        self.responses = responses

    def __call__(self, request: Request) -> Union[JSONResponse, None]:
        status_code = request.headers.get(self.header_key)
        if status_code:
            status_code = int(status_code)
            if 200 <= status_code < 300:
                return JSONResponse(
                    content={
                        "message": "mocked with X-Alice-Mock-Response-Status-Code headers"
                    },
                    status_code=status_code,
                )
            else:
                detail = self.responses.get(status_code) if self.responses else None
                raise HTTPException(status_code=status_code, detail=detail)
