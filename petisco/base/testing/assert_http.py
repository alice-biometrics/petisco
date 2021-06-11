def assert_http(response, expected_status_code: int):
    response_detail = (
        response.json if isinstance(response.json, dict) else response.json()
    )
    assert (
        response.status_code == expected_status_code
    ), f"{response.status_code} - {response_detail}"
