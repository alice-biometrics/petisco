from petisco import Petisco
import os
import pytest

from tests.end2end.flask_app import petisco_config

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


@pytest.fixture
def petisco_yml_path_flask_app():
    return f"{os.path.dirname(os.path.abspath(__file__))}"


@pytest.fixture
def given_petisco_flask_app(petisco_yml_path_flask_app):
    Petisco.clear()
    petisco = Petisco.from_filename(
        f"{petisco_yml_path_flask_app}/flask_app/petisco.yml"
    )
    yield petisco
    Petisco.clear()


@pytest.fixture
def petisco_client_flask_app(given_petisco_flask_app):
    app = given_petisco_flask_app.get_app()
    with app.app.test_client() as c:
        yield c


@pytest.fixture
def given_petisco_flask_app_with_mongodb(petisco_yml_path_flask_app):
    Petisco.clear()
    petisco = Petisco.from_filename(
        f"{petisco_yml_path_flask_app}/flask_app/petisco_with_mongo.yml"
    )
    yield petisco
    Petisco.clear()


@pytest.fixture
def petisco_client_flask_app_with_mongodb(given_petisco_flask_app_with_mongodb):
    app = given_petisco_flask_app_with_mongodb.get_app()
    with app.app.test_client() as c:
        yield c
