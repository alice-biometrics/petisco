import pytest

from tests.integration.flask_app.toy_app import petisco_config

petisco_config()


@pytest.fixture
def given_any_apikey():
    apikey = "apikey"
    return apikey


@pytest.fixture
def given_code_injection_name():
    return "<script>evil()</script>"
