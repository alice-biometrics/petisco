from typing import Any


def assert_http(response: Any, expected_status_code: int) -> None:
    response_detail = response.json if isinstance(response.json, dict) else response.json()
    assert response.status_code == expected_status_code, f"{response.status_code} - {response_detail}"
