import pytest

from petisco import Persistence, MySqlConnection, MySqlDatabase
from petisco.persistence.sql.mysql_is_running_locally import mysql_is_running_locally
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother


@pytest.mark.integration
@pytest.mark.skipif(
    not mysql_is_running_locally(), reason="MySql is not running locally"
)
def test_should_create_persistence_with_mysql_database():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = MySqlConnection.create_local()
    database = MySqlDatabase(
        name="mysql_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.create()
    persistence.delete()
    Persistence.clear()
