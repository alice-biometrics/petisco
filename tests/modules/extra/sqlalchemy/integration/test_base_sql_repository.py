import pytest

from petisco import Persistence
from petisco.extra.sqlalchemy import SqliteConnection, SqliteDatabase
from tests.modules.extra.sqlalchemy.mother.model_filename_mother import (
    ModelFilenameMother,
)
from tests.modules.extra.sqlalchemy.mother.sql_repository_mother import (
    Client,
    SqlRepositoryMother,
    User,
    UserId,
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

    client = Client.random()
    repository = SqlRepositoryMother.with_client("sqlite_test", client)

    user = User(user_id=UserId.v4(), name="user1", client_id=client.client_id)
    repository.save(user)

    retrieved_user = repository.retrieve(user.user_id).unwrap()

    assert user == retrieved_user

    persistence.delete()
    Persistence.clear()
