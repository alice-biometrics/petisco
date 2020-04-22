import pytest

from petisco.application.petisco import Petisco


@pytest.fixture
def petisco_client(petisco_sql_database):
    app = Petisco.get_instance().get_app()
    with app.app.test_client() as c:
        yield c
