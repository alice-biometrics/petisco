import pytest

from petisco.legacy import Persistence, MySqlConnection, MySqlDatabase
from petisco.legacy.fixtures import testing_with_mysql
from tests.modules.legacy.persistence.mother.model_filename_mother import (
    ModelFilenameMother,
)


@pytest.mark.integration
@testing_with_mysql
def test_should_create_persistence_with_mysql_database():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = MySqlConnection.create_local()
    database = MySqlDatabase(
        name="mysql_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)

    persistence.create()

    assert database.info() == {
        "name": "mysql_test",
        "models": {
            "client": "tests.modules.legacy.persistence.ymls.sql.models.ClientModel",
            "product": "tests.modules.legacy.persistence.ymls.sql.models.ProductModel",
            "user": "tests.modules.legacy.persistence.ymls.sql.models.UserModel",
        },
    }

    persistence.delete()
    Persistence.clear()
