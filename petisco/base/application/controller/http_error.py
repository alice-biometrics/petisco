from typing import Any, Dict, Union

from pydantic import BaseModel, Field, field_validator

DEFAULT_HTTP_ERROR_DETAIL = "Unknown Error"


class HttpError(BaseModel):
    status_code: int = Field(default=500)
    detail: str = Field(default=DEFAULT_HTTP_ERROR_DETAIL)
    headers: Union[Dict[str, Any], None] = Field(default=None)
    type_error: Union[str, None] = Field(default=None, validate_default=True)

    @field_validator("type_error", mode="before")
    def prevent_type_error_none(cls, value: Union[str, None]) -> str:
        if value is None:
            value = cls.__name__
        return value
