from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeVar

from petisco.base.domain.persistence.database import Database

T = TypeVar("T")


def get_key(base_type: type[T], alias: str | None = None) -> str:
    return base_type.__name__ if not alias else alias


@dataclass
class _Databases:
    def __init__(self) -> None:
        self._databases: dict[str, Any] = {}

    def __repr__(self) -> str:
        return f"Databases: {str(self.info())}"

    def info(self) -> dict[str, Any]:
        return {name: database.info() for name, database in self._databases.items()}

    # This does no have any sense, we want to check all databases
    # def _get_databases(self, database_name: str | None = None) -> dict[str, Database] | None:
    #     if database_name is not None:
    #         if database_name not in self._databases:
    #             raise IndexError(
    #                 f"Database cannot return are_available/async_are_available. {database_name} not exists"
    #             )
    #         databases_ = {database_name: self._databases.get(database_name)}
    #         return databases_
    #     if len(self._databases) < 1:
    #         logger.warning("Databases databases are empty")
    #         return None
    #
    # def are_available(self, database_name: str | None = None) -> bool:
    #     databases_ = self._get_databases(database_name)
    #     if databases_ is None:
    #         return False
    #
    #     for database_name, database in databases_.items():
    #         if isinstance(database, AsyncDatabase):
    #             continue
    #         if not database.is_available():
    #             logger.warning(f"Database {database_name} is not available")
    #             return False
    #     return True
    #
    # async def async_are_available(self, database_name: str | None = None) -> bool:
    #     databases_ = self._get_databases(database_name)
    #     if databases_ is None:
    #         return False
    #
    #     for database_name, database in databases_.items():
    #         if not isinstance(database, AsyncDatabase):
    #             continue
    #         if not await database.is_available():
    #             logger.warning(f"Database {database_name} is not available")
    #             return False
    #     return True

    def get_databases(self) -> list[Database]:
        return list(self._databases.values())

    def get_database_names(self) -> list[str]:
        return list(self._databases.keys())

    def add(
        self, database: Database | list[Database], skip_if_exist: bool = False
    ) -> None:
        if isinstance(database, list):
            for database_ in database:
                self.add(database_, skip_if_exist)

        elif isinstance(database, Database):
            key = database.get_key()
            if key in self._databases:
                if skip_if_exist is False:
                    raise NameError(f"Database {key} is already added to Databases")
            else:
                self._databases[key] = database
        else:
            raise TypeError(
                f"Databases.add only accept a Database or a list of Database and your input is {database}"
            )

    def get(self, base_type: type[T], *, alias: str | None = None) -> T:
        key = get_key(base_type, alias)
        if key in self._databases:
            return self._databases.get(key)
        else:
            raise NameError(f"Database {key} does not exist in Databases")

    def remove(
        self,
        base_type: type[T],
        *,
        alias: str | None = None,
        skip_if_not_exist: bool = False,
    ) -> None:
        key = get_key(base_type, alias)

        if key in self._databases:
            self._databases[key].delete()
            del self._databases[key]
        else:
            if skip_if_not_exist is False:
                raise IndexError(f"Database cannot be removed. {key} does not exists")

    def initialize(self) -> None:
        for database in self._databases.values():
            database.initialize()

    def delete(self) -> None:
        for database in self._databases.values():
            database.delete()

    def clear_database(self, base_type: type[T], *, alias: str | None = None) -> None:
        key = get_key(base_type, alias)
        databases_ = self._databases
        if key is not None:
            if key not in self._databases:
                raise IndexError(f"Database cannot clear the data. {key} not exists")
            databases_ = [self._databases.get(key)]
        for database in databases_.values():
            database.clear_data()

    def clear(self):
        self._databases = {}


databases = _Databases()
