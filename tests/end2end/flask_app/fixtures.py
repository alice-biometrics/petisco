import os

import pytest

from tests.end2end.flask_app.toy_app import petisco_config

petisco_config()

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
port = (
    int(os.getenv("MONGODB_PORT"))
    if os.getenv("MONGODB_PORT")
    else os.getenv("MONGODB_PORT")
)
host = os.getenv("MONGODB_HOST")
database = os.getenv("MONGODB_DATABASE")


@pytest.fixture
def given_any_apikey():
    apikey = "apikey"
    return apikey


@pytest.fixture
def given_code_injection_name():
    return "<script>evil()</script>"
