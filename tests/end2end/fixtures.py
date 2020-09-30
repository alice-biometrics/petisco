from petisco import Petisco
from .flask_app.fixtures import *  # noqa F403
import pytest
import os


@pytest.fixture
def petisco_yml_path_flask_app():
    return f"{os.path.dirname(os.path.abspath(__file__))}"


@pytest.fixture
def given_petisco_flask_app(petisco_yml_path_flask_app):
    Petisco.clear()
    petisco = Petisco.from_filename(
        f"{petisco_yml_path_flask_app}/flask_app/toy_app/petisco.yml"
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
        f"{petisco_yml_path_flask_app}/flask_app/toy_app/petisco_with_mongo.yml"
    )
    yield petisco
    Petisco.clear()


@pytest.fixture
def petisco_client_flask_app_with_mongodb(given_petisco_flask_app_with_mongodb):
    app = given_petisco_flask_app_with_mongodb.get_app()
    with app.app.test_client() as c:
        yield c
