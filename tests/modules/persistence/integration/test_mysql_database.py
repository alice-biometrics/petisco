import pytest

from petisco import Persistence, MySqlConnection, MySqlDatabase
from petisco.fixtures import testing_with_mysql
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother


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
    persistence.delete()
    Persistence.clear()
