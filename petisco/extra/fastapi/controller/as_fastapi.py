from __future__ import annotations

from typing import TypeVar

from meiga import AnyResult

T = TypeVar("T")


def as_fastapi(result: AnyResult, expected_type: type[T] | None = None) -> T:
    """
    Transforms Controller Result to mapped value (Takes Config Controller configurations)
    """
    return result.transform(expected_type=expected_type)
