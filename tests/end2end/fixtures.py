from petisco import Petisco, Persistence, SqliteDatabase, SqliteConnection
import os
import pytest

# from tests.end2end.flask_app import petisco_config
# petisco_config()
from tests.end2end.flask_app.config.app_services import load_app_services
from tests.end2end.flask_app.config.repositories import load_repositories

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
    return f"{os.path.dirname(os.path.abspath(__file__))}/flask_app"


@pytest.fixture
def petisco_yml_path_end2end():
    return f"{os.path.dirname(os.path.abspath(__file__))}/ymls"


@pytest.fixture
def given_petisco_flask_app(petisco_yml_path_flask_app):
    Petisco.clear()
    petisco = Petisco.from_filename(f"{petisco_yml_path_flask_app}/petisco.yml")
    petisco.configure_events(petisco_yml_path_flask_app + "/petisco.events.yml")

    load_app_services()
    sql_database = SqliteDatabase(
        name="petisco-sql",
        connection=SqliteConnection.create("sqlite", "petisco-test.db"),
        model_filename=f"{petisco_yml_path_flask_app}/petisco.sql.models.yml",
    )
    persistence = Persistence()
    persistence.add(sql_database, skip_if_exist=True)
    persistence.create()
    load_repositories()

    yield petisco

    persistence.clear_data()

    Petisco.clear()
    petisco.stop()


@pytest.fixture
def client_app(given_petisco_flask_app):
    app = given_petisco_flask_app.get_app()
    with app.app.test_client() as c:
        yield c


@pytest.fixture
def given_petisco_flask_app_with_mongodb(petisco_yml_path_flask_app):
    Petisco.clear()
    petisco = Petisco.from_filename(
        f"{petisco_yml_path_flask_app}/petisco_with_mongo.yml"
    )
    petisco.configure_events(petisco_yml_path_flask_app + "/petisco.events.yml")
    yield petisco
    Petisco.clear()
    petisco.stop()


@pytest.fixture
def client_app_with_mongodb(given_petisco_flask_app_with_mongodb):
    app = given_petisco_flask_app_with_mongodb.get_app()
    with app.app.test_client() as c:
        yield c
