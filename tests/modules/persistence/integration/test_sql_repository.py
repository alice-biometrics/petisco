import pytest

from petisco import SqliteDatabase, SqliteConnection, Persistence
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother
from tests.modules.persistence.mother.sql_repository_mother import (
    SqlRepositoryMother,
    User,
)


@pytest.mark.integration
def test_should_save_a_model_using_a_sql_repository_implementation():
    filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
    connection = SqliteConnection.create(
        server_name="sqlite", database_name="petisco.db"
    )
    database = SqliteDatabase(
        name="sqlite_test", connection=connection, model_filename=filename
    )

    persistence = Persistence()
    persistence.add(database)
    persistence.create()

    repository = SqlRepositoryMother.user("sqlite_test")

    user = User.random()
    repository.save(user)

    retrieved_user = repository.retrieve(user.user_id).unwrap()

    assert user == retrieved_user

    persistence.delete()
    Persistence.clear()
