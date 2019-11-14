import os

import pytest


from petisco import FlaskApplication

SWAGGER_DIR = os.path.dirname(os.path.abspath(__file__)) + "/application/"
app = FlaskApplication(application_name="petisco", swagger_dir=SWAGGER_DIR).get_app()


@pytest.fixture
def client():
    with app.app.test_client() as c:
        yield c


@pytest.fixture
def given_any_apikey():
    apikey = "apikey"
    return apikey
