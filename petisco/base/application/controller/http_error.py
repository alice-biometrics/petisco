from typing import Optional

from pydantic import BaseModel, validator

DEFAULT_HTTP_ERROR_DETAIL = "Unknown Error"


class HttpError(BaseModel):
    status_code: Optional[int] = 500
    detail: Optional[str] = DEFAULT_HTTP_ERROR_DETAIL
    headers: Optional[dict] = None
    type_error: Optional[str] = None

    @validator("type_error", always=True)
    def prevent_type_error_none(cls, value):
        if value is None:
            value = cls.__name__
        return value
