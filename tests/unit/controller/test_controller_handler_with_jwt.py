import pytest
from meiga import Success

from petisco import controller_handler, INFO, ERROR
from petisco.controller.tokens.jwt_config import JwtConfig
from tests.unit.mocks.fake_logger import FakeLogger
from tests.unit.mocks.log_message_mother import LogMessageMother


@pytest.fixture
def given_any_token_type():
    return "TOKEN"


@pytest.fixture
def given_other_token_type():
    return "REQUIRED_TOKEN"


@pytest.fixture
def given_any_token_type_with_user():
    return "USER_TOKEN"


@pytest.fixture
def given_any_client_id():
    return "client_id"


@pytest.fixture
def given_any_user_id():
    return "user_id"


@pytest.fixture
def given_any_decoded_token_info(given_any_token_type, given_any_client_id):
    return {
        "user_id": None,
        "client_id": given_any_client_id,
        "token_type": given_any_token_type,
    }


@pytest.fixture
def given_any_decoded_token_info_with_user(
    given_any_token_type_with_user, given_any_client_id, given_any_user_id
):
    return {
        "user_id": given_any_user_id,
        "client_id": given_any_client_id,
        "token_type": given_any_token_type_with_user,
    }


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_jwt_requirement_without_user(
    given_any_token_type, given_any_decoded_token_info
):

    logger = FakeLogger()
    jwt_config = JwtConfig(token_type=given_any_token_type)

    @controller_handler(logger=logger, jwt_config=jwt_config)
    def my_controller(token_info):
        return Success("Hello Petisco")

    http_response = my_controller(token_info=given_any_decoded_token_info)

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_jwt_requirement_with_user(
    given_any_token_type_with_user, given_any_decoded_token_info_with_user
):

    logger = FakeLogger()
    jwt_config = JwtConfig(token_type=given_any_token_type_with_user, require_user=True)

    @controller_handler(logger=logger, jwt_config=jwt_config)
    def my_controller(token_info, user_id):
        return Success("Hello Petisco")

    http_response = my_controller(token_info=given_any_decoded_token_info_with_user)

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_returns_an_error_when_a_empty_controller_do_not_get_a_required_jwt_token(
    given_other_token_type, given_any_decoded_token_info
):

    logger = FakeLogger()
    jwt_config = JwtConfig(token_type=given_other_token_type)

    @controller_handler(logger=logger, jwt_config=jwt_config)
    def my_controller(token_info):
        return Success("Hello Petisco")

    http_response = my_controller(token_info=given_any_decoded_token_info)

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
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: InvalidTokenError: This entry point expects a valid REQUIRED_TOKEN Token]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_returns_an_error_when_a_empty_controller_get_a_required_jwt_token_but_missing_user(
    given_any_token_type, given_any_decoded_token_info
):

    logger = FakeLogger()
    jwt_config = JwtConfig(token_type=given_any_token_type, require_user=True)

    @controller_handler(logger=logger, jwt_config=jwt_config)
    def my_controller(token_info):
        return Success("Hello Petisco")

    http_response = my_controller(token_info=given_any_decoded_token_info)

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
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: InvalidTokenError: This entry point expects a valid TOKEN Token]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_jwt_requirement_without_user_without_defining_token_info_arg(
    given_any_token_type, given_any_decoded_token_info
):

    logger = FakeLogger()
    jwt_config = JwtConfig(token_type=given_any_token_type)

    @controller_handler(logger=logger, jwt_config=jwt_config)
    def my_controller():
        return Success("Hello Petisco")

    http_response = my_controller(token_info=given_any_decoded_token_info)

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )
