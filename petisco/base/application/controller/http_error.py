from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

DEFAULT_HTTP_ERROR_DETAIL = "Unknown Error"


class HttpError(BaseModel):
    status_code: int = Field(default=500)
    detail: str = Field(default=DEFAULT_HTTP_ERROR_DETAIL)
    headers: dict[str, Any] = Field(default=None)
    type_error: str = Field(default=None, validate_default=True)

    @field_validator("type_error", mode="before")
    def prevent_type_error_none(cls, value: str | None) -> str:
        if value is None:
            value = cls.__name__
        return value
