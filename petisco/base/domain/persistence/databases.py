from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeVar

from petisco.base.domain.persistence.async_database import AsyncDatabase
from petisco.base.domain.persistence.database import Database

T = TypeVar("T")


def get_key(base_type: type[T], alias: str | None = None) -> str:
    return alias if alias else base_type.__name__


@dataclass
class _Databases:
    def __init__(self) -> None:
        self._databases: dict[str, Any] = {}

    def __repr__(self) -> str:
        return f"Databases: {str(self.info())}"

    def info(self) -> dict[str, Any]:
        return {name: database.info() for name, database in self._databases.items()}

    def get_databases(self) -> list[Database[Any]]:
        return list(self._databases.values())

    def get_database_names(self) -> list[str]:
        return list(self._databases.keys())

    def add(self, database: Database | list[Database], skip_if_exist: bool = False) -> None:
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

    def initialize(self, initialization_arguments: dict[str, dict[str, Any]] | None = None) -> None:
        for database in self._databases.values():
            if isinstance(database, AsyncDatabase):
                continue
            arguments = initialization_arguments.get(database.alias) if initialization_arguments else None
            if arguments:
                database.initialize(**arguments)
            else:
                database.initialize()

    async def async_initialize(
        self, initialization_arguments: dict[str, dict[str, Any]] | None = None
    ) -> None:
        for database in self._databases.values():
            if isinstance(database, AsyncDatabase):
                arguments = initialization_arguments.get(database.alias) if initialization_arguments else None
                if arguments:
                    await database.initialize(**arguments)
                else:
                    await database.initialize()

    def delete(self) -> None:
        for database in self._databases.values():
            database.delete()

    def clear_database(self, base_type: type[T], *, alias: str | None = None) -> None:
        key = get_key(base_type, alias)
        databases_ = self._databases
        if key is not None and key not in self._databases:
            raise IndexError(f"Database cannot clear the data. {key} not exists")
        for database in databases_.values():
            database.clear_data()

    def clear(self) -> None:
        self._databases = {}


databases = _Databases()
