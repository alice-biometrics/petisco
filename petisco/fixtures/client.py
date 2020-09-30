import pytest


@pytest.fixture
def petisco_client(given_any_petisco, petisco_sql_database):
    app = given_any_petisco.get_app()
    with app.app.test_client() as c:
        yield c
