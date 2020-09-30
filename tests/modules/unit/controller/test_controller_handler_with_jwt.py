import pytest
from meiga import Success

from petisco import controller_handler, ERROR, InfoId, DEBUG
from petisco.security.token_manager.token_manager import TokenManager
from tests.modules.unit.mocks.fake_logger import FakeLogger
from tests.modules.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_jwt_requirement_without_user(
    given_any_petisco,
    given_any_token_type,
    given_any_headers_provider_with_correlation_id,
    given_any_client_id,
    given_any_correlation_id,
):

    logger = FakeLogger()
    expected_info_id = InfoId(
        client_id=given_any_client_id,
        user_id=None,
        correlation_id=given_any_correlation_id,
    )

    @controller_handler(
        logger=logger,
        token_manager=TokenManager(token_type=given_any_token_type),
        headers_provider=given_any_headers_provider_with_correlation_id,
    )
    def my_controller(info_id: InfoId):
        assert info_id == expected_info_id
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=expected_info_id,
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
            info_id=expected_info_id,
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_jwt_requirement_with_user(
    given_any_petisco,
    given_any_token_type_with_user,
    given_headers_provider,
    given_auth_token_headers_creator,
    given_any_client_id,
    given_any_user_id,
    given_any_correlation_id,
    given_info_id_only_correlation_id,
):

    logger = FakeLogger()
    expected_info_id = InfoId(
        client_id=given_any_client_id,
        user_id=given_any_user_id,
        correlation_id=given_any_correlation_id,
    )

    @controller_handler(
        logger=logger,
        token_manager=TokenManager(
            token_type=given_any_token_type_with_user, require_user=True
        ),
        headers_provider=given_headers_provider(
            {
                **given_auth_token_headers_creator(
                    given_any_token_type_with_user,
                    given_any_client_id,
                    given_any_user_id,
                ),
                **given_info_id_only_correlation_id.get_http_headers(),
            }
        ),
    )
    def my_controller(info_id: InfoId):
        assert info_id == expected_info_id
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=expected_info_id,
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
            info_id=expected_info_id,
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_returns_an_error_when_a_empty_controller_do_not_get_a_required_jwt_token(
    given_any_petisco,
    given_other_token_type,
    given_any_info_id,
    given_headers_provider,
    given_auth_token_headers_creator,
    given_any_client_id,
    given_any_user_id,
    given_info_id_only_correlation_id,
):

    logger = FakeLogger()

    @controller_handler(
        logger=logger,
        token_manager=TokenManager(token_type=given_other_token_type),
        headers_provider=given_headers_provider(
            {
                **given_auth_token_headers_creator(
                    "INVALID_TOKEN_TYPE", given_any_client_id, given_any_user_id
                ),
                **given_info_id_only_correlation_id.get_http_headers(),
            }
        ),
    )
    def my_controller():
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == (
        {
            "error": {
                "message": "Access token is missing or invalid. This entry point expects a valid REQUIRED_TOKEN Token",
                "type": "InvalidTokenHttpError",
            }
        },
        401,
    )

    first_logging_message = logger.get_logging_messages()[0]

    assert first_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: InvalidTokenError: This entry point expects a valid REQUIRED_TOKEN Token]",
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_returns_an_error_when_a_empty_controller_get_a_required_jwt_token_but_missing_user(
    given_any_petisco,
    given_any_token_type,
    given_headers_provider,
    given_auth_token_headers_creator,
    given_any_token_type_with_user,
    given_any_client_id,
    given_info_id_only_correlation_id,
):
    logger = FakeLogger()

    @controller_handler(
        logger=logger,
        token_manager=TokenManager(token_type=given_any_token_type, require_user=True),
        headers_provider=given_headers_provider(
            {
                **given_auth_token_headers_creator(
                    given_any_token_type_with_user, given_any_client_id, None
                ),
                **given_info_id_only_correlation_id.get_http_headers(),
            }
        ),
    )
    def my_controller():
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == (
        {
            "error": {
                "message": "Access token is missing or invalid. This entry point expects a valid TOKEN Token",
                "type": "InvalidTokenHttpError",
            }
        },
        401,
    )

    first_logging_message = logger.get_logging_messages()[0]

    assert first_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: InvalidTokenError: This entry point expects a valid TOKEN Token]",
        ).to_dict(),
    )
