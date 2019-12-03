import os

import pytest
from sqlalchemy import create_engine

from petisco import FlaskApplication, SqlAlchemyPersistence
from petisco.controller.tokens.jwt_token_builder import JwtTokenBuilder
from tests.integration.flask_app.key import KEY

SWAGGER_DIR = os.path.dirname(os.path.abspath(__file__)) + "/toy_app/"
app = FlaskApplication(application_name="petisco", swagger_dir=SWAGGER_DIR).get_app()


@pytest.fixture
def client():
    with app.app.test_client() as c:
        yield c


@pytest.fixture
def database():

    connection = "sqlite:///petisco.db"
    engine = create_engine(connection)

    Base = SqlAlchemyPersistence.get_instance().base
    Session = SqlAlchemyPersistence.get_instance().session

    Base.metadata.create_all(engine)

    yield

    session = Session()
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)
    os.remove("petisco.db")


@pytest.fixture
def given_any_apikey():
    apikey = "apikey"
    return apikey


@pytest.fixture
def given_any_name():
    return "Any Name"


@pytest.fixture
def given_code_injection_name():
    return "<script>evil()</script>"


@pytest.fixture
def given_any_user_id():
    return "12345678910"


@pytest.fixture
def given_auth_token_headers_creator():
    def _given_auth_token_headers_creator(
        type_token=str, client_id="client_id", user_id=None
    ):

        headers = {
            "Authorization": f"Bearer {JwtTokenBuilder.build(KEY, type_token, client_id, user_id=user_id)}"
        }
        return headers

    return _given_auth_token_headers_creator
