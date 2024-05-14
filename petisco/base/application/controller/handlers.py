from __future__ import annotations

from typing import Any, Callable

from meiga import AnyResult, Result


def unwrap_result_handler(result: AnyResult) -> Any:
    assert isinstance(result, Result), "result_handler input must be a Result"
    return result.unwrap()


def custom_message_handler(message: dict[str, Any]) -> Callable[[AnyResult], dict[str, Any]]:
    def _result_handler(_: AnyResult) -> dict[str, Any]:
        return message

    return _result_handler
