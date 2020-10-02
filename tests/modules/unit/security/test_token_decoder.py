import pytest

from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from petisco.security.token_decoder.token_decoder import TokenDecoder


@pytest.mark.unit
@pytest.mark.parametrize(
    "type_token,client_id,user_id",
    [
        ("ADMIN_TOKEN", ClientId("client-id"), None),
        ("ADMIN_TOKEN", ClientId("client-id"), UserId("user-id")),
        ("BACKEND_TOKEN", ClientId("client-id"), UserId("user-id")),
    ],
)
def test_should_decode_a_token_successfully(
    type_token, client_id, user_id, given_auth_token_headers_creator
):
    auth_token = given_auth_token_headers_creator(type_token, client_id, user_id)[
        "Authorization"
    ]

    token_decoder = TokenDecoder()
    token = token_decoder.execute(auth_token).unwrap()

    assert token.token_type == type_token
    assert token.client_id == client_id
    assert token.user_id == user_id
