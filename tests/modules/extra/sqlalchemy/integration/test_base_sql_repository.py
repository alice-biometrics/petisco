import pytest
from meiga.assertions import assert_failure

from petisco import databases
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
)
from petisco.base.domain.errors.defaults.not_found import (
    AggregateNotFoundError,
    AggregatesNotFoundError,
)
from petisco.extra.sqlalchemy import SqlDatabase, SqliteConnection
from tests.modules.extra.sqlalchemy.mother.sql_repository_mother import (
    Client,
    SqlRepositoryMother,
    User,
    UserId,
)


@pytest.mark.integration
class TestBaseSqlRepository:
    client: Client

    def setup_method(self):
        self._configure_db()
        self.client = Client.random()

    def _configure_db(self) -> None:
        # filename = ModelFilenameMother.get("sql/persistence.sql.models.yml")
        connection = SqliteConnection.create(server_name="sqlite", database_name="petisco.db")
        databases.add(SqlDatabase(connection=connection))
        databases.initialize()

    def teardown_method(self) -> None:
        databases.remove(SqlDatabase)

    def should_save_a_model_using_a_sql_repository_implementation(self):
        repository = SqlRepositoryMother.with_client(self.client)

        user = User(user_id=UserId.v4(), name="user1", client_id=self.client.client_id)
        repository.save(user)

        retrieved_user = repository.retrieve(user.user_id).unwrap()

        assert user == retrieved_user

    def should_raise_aggregate_already_exist_error(self):
        user = User(user_id=UserId.v4(), name="user1", client_id=self.client.client_id)
        repository = SqlRepositoryMother.with_user(user, self.client)

        result = repository.save(user)

        assert_failure(result, value_is_instance_of=AggregateAlreadyExistError)

    def should_raise_aggregate_not_found_error(self):
        repository = SqlRepositoryMother.with_client(self.client)

        result = repository.retrieve(UserId.v4())

        assert_failure(result, value_is_instance_of=AggregateNotFoundError)

    def should_raise_aggregates_not_found_error(self):
        repository = SqlRepositoryMother.with_client(self.client)

        result = repository.retrieve_all(self.client.client_id)

        assert_failure(result, value_is_instance_of=AggregatesNotFoundError)
