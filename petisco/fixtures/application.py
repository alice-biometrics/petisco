import pytest

from typing import Dict

from petisco import ROOT_PATH, ClientId, UserId
from petisco.application.config.config import Config
from petisco.application.petisco import Petisco
from petisco.security.token_manager.jwt_token_builder import JwtTokenBuilder


@pytest.fixture
def given_petisco_version():
    return open(f"{ROOT_PATH}/VERSION", "r").read()[:-1]


@pytest.fixture
def given_headers_provider():
    def _given_headers_provider(headers: Dict):
        return lambda: headers

    return _given_headers_provider


@pytest.fixture
def given_any_headers_provider_with_correlation_id(
    given_any_header_with_valid_token,
    given_headers_provider,
    given_info_id_only_correlation_id,
):
    headers_token = given_any_header_with_valid_token
    headers_correlation = given_info_id_only_correlation_id.get_http_headers()
    return given_headers_provider({**headers_token, **headers_correlation})


@pytest.fixture
def given_any_headers_provider_with_info_id(
    given_any_header_with_valid_token, given_headers_provider, given_any_info_id
):
    headers_token = given_any_header_with_valid_token
    headers_correlation = given_any_info_id.get_http_headers()
    return given_headers_provider({**headers_token, **headers_correlation})


@pytest.fixture
def given_any_headers_provider(
    given_any_header_with_valid_token, given_headers_provider
):
    return given_headers_provider(given_any_header_with_valid_token)


@pytest.fixture
def given_any_headers_provider_with_user(
    given_any_header_with_valid_token_with_user_id, given_headers_provider
):
    return given_headers_provider(given_any_header_with_valid_token_with_user_id)


@pytest.fixture
def given_dummy_key():
    return (
        "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9b6fIsGAjrg7X"
        "\ncwnQWHUA1R1DCbB2oMQRmfrUVe2i3bIdjJ3ATgAcEAr+LDYas1tLM/zh/wLBYFzT\nCKfdFhn6YNfMHbbjcj"
        "+GfPM0kCnNtomsMUlDvHhqwLMEg8Af8r0cWorBWVrzM7Ab\nl1c9lhGR64U5oUCSSC27m+JxJFzc"
        "/FRe1dH4Dad1G9qx25DdZJoCuZfIqdYMGbt1\nzSaqXa9I4RTVPtzp4cYUG4iZ42+Gcn"
        "/dNrtgjXA5EPP3aGDoVNZWnlF4r8SSEQ3z\nMvNpRDtbGSrw5rKGYfW21da+7sqhvU/Q0DOeURAY4YuOaw+/Y3BoU"
        "/EFPcrZ344u\nRe5v5iwVAgMBAAECggEADYuERbdGyIZTjVguZXVNuGeElhyFP5YzLscBxlj2iuSr\nLa22Qd/R5i"
        "/HeXET1UjpyDDJbidbvRP0zyoZRpej9+EgzPl68DxlCmq4wRNlyc25"
        "\nflRv1qYNPiTVKAd7n00t9G8M6NJIzIbvmqlxlXe7feGHPx2mjk8W5gk5Ybml4i8Q"
        "\n5wfRAwCLmitLwuUlpNX5lcDPudAcOwO7ik854y1LwMs3necpQ4qyjLUFIeMxoq1u"
        "\nJCUn3ReCKwpTGcKNcPM6tf9yhhnZi1Lntytcdli9TqsJK0dRnczVuc6W+hCX/Szu\n9x57waLc+6w1i87aOn/XqzoS"
        "+R02Ct3emM1hbAd5gQKBgQD41sfsbM6inxQTvdF0\n1p2pF1Fw3VyymmL3dNMUNzD2GgbiLISGtzfvaIFLJn/OLRp"
        "+9XBIjtkFcpdsKktD\ngIjGf3DXI/hFV7doj1jB7udAhyegt7XZWo3JXcPNTlTXXf/dVGptIsfjMeo+9UEn\nZuIueJki"
        "/SEjtnZposBFS+efUQKBgQDC4z+bv2NeuCcjmMGjuvhp4xTQWY4lkWbd\ndaBbhh8fxlhfZSlkXQ8efNyuDMZR0EV"
        "+XGVQf1sU3Zx8iuuNwOsAXhtr0uTALKr9\nO3nYOik1bKwq7hn2uFCJ8zisNDQBlypflK8Kw7lTcTnh2UdMBxnjCfdvIK+L7Yyu"
        "\nnXE3bnY3hQKBgBpZxDoJG6ik599fTnrs7y0kxv8IsfRH3QsPV/rgDVNCVlBFHpOV\ne1ri2i43GXmf1Rp0qztDxT"
        "+KbvaJVAcF6XX7sNtXd8cADvAHngKLZfmzVkLysVMe\n/7y/LSjkjp9v2NR7R/neoQQyGPgpyIh/oJwDMVQ/Me8yNz"
        "/geDPeYdzBAoGARZWu\nWIX1jRRjpSoducBAgk46WEohnvhTqi8dmpBA/K9tTmJobRVtGI2sndih1wRuS7fh"
        "\n1OQkOUcHYNCZWnvPbMotMEqUsqlARDrAPpxFqnWq44kwbA9Tcm4Nhi79grPexVHp"
        "\nTgakXU7IRAO4mUTP0Wj1mBArneKroI1Gp2wheaECgYEA7rakdIlHHE3DnVeFnMd0\ngYrzBFRi"
        "+8IXssPRuFvou93tkFI7huEzz46SL1Igx9G/q5enA/1GSzKlIDBbebXx\nGzF/urX+jE+TaR3U8LUaV8dMFk3yF+bR2nnJabv"
        "+DMvyxJtUYiEnFgCypbG5m89Y\n9FHLq/CZ1uLCQhY1ITq/kTM=\n-----END PRIVATE KEY----- "
    )


@pytest.fixture
def given_auth_token_headers_creator(given_dummy_key):
    def _given_auth_token_headers_creator(
        type_token=str,
        client_id: ClientId = ClientId("client-id"),
        user_id: UserId = None,
    ):
        headers = {
            "Authorization": f"Bearer {JwtTokenBuilder.build(given_dummy_key, type_token, client_id, user_id=user_id)}"
        }
        return headers

    return _given_auth_token_headers_creator


@pytest.fixture
def given_any_header_with_valid_token(
    given_auth_token_headers_creator, given_any_token_type, given_any_client_id
):
    return given_auth_token_headers_creator(
        type_token=given_any_token_type, client_id=given_any_client_id
    )


@pytest.fixture
def given_any_header_with_valid_token_with_user_id(
    given_auth_token_headers_creator,
    given_any_token_type,
    given_any_client_id,
    given_any_user_id,
):
    return given_auth_token_headers_creator(
        type_token=given_any_token_type,
        client_id=given_any_client_id,
        user_id=given_any_user_id,
    )


@pytest.fixture
def given_any_petisco():
    return Petisco(config=Config(app_name="petisco", app_version="1.0.0"))
