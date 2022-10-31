from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, validator

DEFAULT_HTTP_ERROR_DETAIL = "Unknown Error"


class HttpError(BaseModel):
    status_code: Union[int, None] = 500
    detail: Optional[str] = DEFAULT_HTTP_ERROR_DETAIL
    headers: Optional[Dict[str, Any]] = None
    type_error: Optional[str] = None

    @validator("type_error", always=True)
    @classmethod
    def prevent_type_error_none(cls, value: Union[str, None]) -> str:
        if value is None:
            value = cls.__name__
        return value
