import pytest
from meiga import Success

from petisco import controller_handler, TokenManager, InfoId, Petisco


@pytest.mark.unit
def test_should_execute_a_controller_without_any_input(given_any_petisco):
    @controller_handler()
    def my_controller():
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_a_controller_with_a_string_parameter(given_any_petisco):
    @controller_handler()
    def my_controller(param: str):
        assert isinstance(param, str)
        return Success("Hello Petisco")

    http_response = my_controller("param")

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_a_controller_with_default_headers_parameter(given_any_petisco,):
    @controller_handler()
    def my_controller(headers):
        assert isinstance(headers, dict)
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_a_controller_with_default_token_info_parameter(
    given_any_petisco, given_any_token_type, given_any_headers_provider
):
    @controller_handler(
        token_manager=TokenManager(token_type=given_any_token_type),
        headers_provider=given_any_headers_provider,
    )
    def my_controller():
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_a_controller_without_token_info_parameter(
    given_any_petisco, given_any_token_type, given_any_headers_provider
):
    @controller_handler(
        token_manager=TokenManager(token_type=given_any_token_type),
        headers_provider=given_any_headers_provider,
    )
    def my_controller(info_id):
        assert isinstance(info_id, InfoId)
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_a_controller_without_receive_any_param(
    given_any_petisco, given_any_token_type, given_any_headers_provider
):
    @controller_handler(
        token_manager=TokenManager(token_type=given_any_token_type),
        headers_provider=given_any_headers_provider,
    )
    def my_controller(info_id: InfoId):
        assert isinstance(info_id, InfoId)
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_a_controller_getting_the_petisco(given_any_petisco):
    @controller_handler()
    def my_controller(petisco):
        assert isinstance(petisco, Petisco)
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)
