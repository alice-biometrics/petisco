from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable

from loguru import logger

from petisco.base.domain.persistence.async_database import AsyncDatabase
from petisco.base.domain.persistence.database import Database
from petisco.base.misc.singleton import Singleton


@dataclass
class Databases(metaclass=Singleton):
    def __init__(self) -> None:
        self._databases: dict[str, Any] = {}

    def __repr__(self) -> str:
        return f"Databases: {str(self.get_info())}"

    @staticmethod
    def get_instance() -> Databases:
        try:
            return Databases()
        except Exception as e:  # noqa E722
            frame_info = inspect.stack()[1]
            raise ImportError(
                f"Databases must be configured. If not, you cannot obtain models\n"
                f"Following code must be executed after Databases initialization:\n"
                f"\tfilename: {frame_info.filename}\n"
                f"\tlineno: {frame_info.lineno}\n"
                f"\tfunction: {frame_info.function}\n"
                f"\tcode_context: {frame_info.code_context}\n\n"
            )

    @staticmethod
    def info() -> dict[str, Any]:
        return Databases.get_instance().get_info()

    @staticmethod
    def _get_databases(database_name: str | None = None) -> dict[str, Database] | None:
        databases = Databases.get_instance()._databases
        if database_name is not None:
            if database_name not in databases:
                raise IndexError(
                    f"Database cannot return is_available. {database_name} not exists"
                )
            databases = {database_name: databases.get(database_name)}
        if len(databases) < 1:
            logger.warning("Databases databases are empty")
            return None
        return databases

    @staticmethod
    def are_available(database_name: str | None = None) -> bool:
        databases = Databases._get_databases(database_name)
        if databases is None:
            return False

        for database_name, database in databases.items():
            if isinstance(database, AsyncDatabase):
                continue
            if not database.is_available():
                logger.warning(f"Database {database_name} is not available")
                return False
        return True

    @staticmethod
    async def async_are_available(database_name: str | None = None) -> bool:
        databases = Databases._get_databases(database_name)
        if databases is None:
            return False

        for database_name, database in databases.items():
            if not isinstance(database, AsyncDatabase):
                continue
            if not await database.is_available():
                logger.warning(f"Database {database_name} is not available")
                return False
        return True

    @staticmethod
    def get_databases() -> list[Database]:
        return list(Databases.get_instance()._databases.values())

    @staticmethod
    def get_available_databases() -> list[str]:
        return list(Databases.get_instance()._databases.keys())

    @staticmethod
    def get_session(database_name: str) -> Any:
        database = Databases.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_session"):
            raise IndexError(f"Database ({database_name}) has not get_session method. ")

        return database.get_session()

    @staticmethod
    def get_session_scope(database_name: str) -> Callable[..., Any]:
        database = Databases.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_session_scope"):
            raise IndexError(
                f"Database ({database_name}) has not get_session_scope method. "
            )

        return database.get_session_scope()

    @staticmethod
    def exist() -> bool:
        databases = Databases.get_instance()._databases
        if len(databases) < 1:
            return False
        else:
            return True

    def get_info(self) -> dict[str, Any]:
        return {name: database.info() for name, database in self._databases.items()}

    def add(self, database: Database, skip_if_exist: bool = False) -> None:
        if database.name in self._databases:
            if skip_if_exist is False:
                raise NameError(
                    f"Database {database.name} is already added to Databases"
                )
        else:
            self._databases[database.name] = database

    def remove(self, database_name: str, skip_if_not_exist: bool = False) -> None:
        if database_name in self._databases:
            self._databases[database_name].delete()
            del self._databases[database_name]
        else:
            if skip_if_not_exist is False:
                raise IndexError(
                    f"Database cannot be removed. {database_name} not exists"
                )

    def initialize(self) -> None:
        for database in self._databases.values():
            database.initialize()

    def delete(self) -> None:
        for database in self._databases.values():
            database.delete()

    def clear_data(self, database_name: str | None = None) -> None:
        databases = self._databases
        if database_name is not None:
            if database_name not in self._databases:
                raise IndexError(
                    f"Database cannot clear the data. {database_name} not exists"
                )
            databases = [self._databases.get(database_name)]
        for database in databases.values():
            database.clear_data()
