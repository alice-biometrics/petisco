from __future__ import annotations

from typing import Any

from meiga import BoolResult, Error, Failure, isSuccess

from petisco import Uuid
from petisco.base.application.patterns.repository import Repository
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
)
from petisco.base.domain.errors.defaults.not_found import (
    AggregateNotFoundError,
    AggregatesNotFoundError,
)
from petisco.base.domain.persistence.databases import databases
from petisco.extra.sqlalchemy.sql.sql_database import SqlDatabase, SqlSessionScope


class SqlRepository(Repository):
    session_scope: SqlSessionScope

    def __init__(self, database_alias: str | None = None):
        """
        Constructs the SqlRepository from a database_alias creating a session_scope (SqlSessionScope)

        Args:
            database_alias (str): A str you defined in database_alias the DatabaseConfigurer
        """
        database = databases.get(SqlDatabase, alias=database_alias)
        self.session_scope = database.get_session_scope()

    @classmethod
    def fail_if_aggregate_already_exist(
        cls, model: Any, aggregate_id: Uuid, result_error: Error | None = None
    ) -> BoolResult:
        if model:
            error = (
                AggregateAlreadyExistError(
                    aggregate_id, cls.__name__, model.__tablename__
                )
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess

    @classmethod
    def fail_if_aggregate_not_found(
        cls, model: Any, aggregate_id: Uuid, result_error: Error | None = None
    ) -> BoolResult:
        if not model:
            error = (
                AggregateNotFoundError(aggregate_id, cls.__name__)
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess

    @classmethod
    def fail_if_aggregates_not_found(
        cls, model: Any, result_error: Error | None = None
    ) -> BoolResult:
        if not model:
            error = (
                AggregatesNotFoundError(cls.__name__)
                if not result_error
                else result_error
            )
            return Failure(error)
        return isSuccess
