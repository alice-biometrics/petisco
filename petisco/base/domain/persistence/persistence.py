import inspect
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union

from loguru import logger

from petisco.base.domain.persistence.interface_database import Database
from petisco.base.misc.singleton import Singleton


@dataclass
class Persistence(metaclass=Singleton):
    def __init__(self) -> None:
        self._databases: Dict[str, Any] = {}

    def __repr__(self) -> str:
        return f"Persistence: {str(self.get_info())}"

    def get_info(self) -> Dict[str, Any]:
        return {name: database.info() for name, database in self._databases.items()}

    @staticmethod
    def info() -> Dict[str, Any]:
        return Persistence.get_instance().get_info()

    @staticmethod
    def get_instance() -> "Persistence":
        try:
            return Persistence()
        except Exception as e:  # noqa E722
            frame_info = inspect.stack()[1]
            raise ImportError(
                f"Persistence must be configured. If not, you cannot obtain models\n"
                f"Following code must be executed after Persistence initialization:\n"
                f"\tfilename: {frame_info.filename}\n"
                f"\tlineno: {frame_info.lineno}\n"
                f"\tfunction: {frame_info.function}\n"
                f"\tcode_context: {frame_info.code_context}\n\n"
            )

    def add(self, database: Database, skip_if_exist: bool = False) -> None:
        if database.name in self._databases:
            if skip_if_exist is False:
                raise NameError(
                    f"Database {database.name} is already added to Persistence"
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

    def create(self) -> None:
        for database in self._databases.values():
            database.create()

    def delete(self) -> None:
        for database in self._databases.values():
            database.delete()

    def clear_data(self, database_name: Union[str, None] = None) -> None:
        databases = self._databases
        if database_name is not None:
            if database_name not in self._databases:
                raise IndexError(
                    f"Database cannot clear the data. {database_name} not exists"
                )
            databases = [self._databases.get(database_name)]
        for database in databases.values():
            database.clear_data()

    @staticmethod
    def exist() -> bool:
        databases = Persistence.get_instance()._databases
        if len(databases) < 1:
            return False
        else:
            return True

    @staticmethod
    def is_available(database_name: Union[str, None] = None) -> bool:
        def log_warning(message: str) -> None:
            logger.debug(message)

        databases = Persistence.get_instance()._databases
        if database_name is not None:
            if database_name not in databases:
                raise IndexError(
                    f"Database cannot return is_available. {database_name} not exists"
                )
            databases = {database_name: databases.get(database_name)}
        if len(databases) < 1:
            log_warning("Persistence databases are empty")
            return False
        for database_name, database in databases.items():
            if not database.is_available():
                log_warning(f"Database {database_name} is not available")
                return False
        return True

    @staticmethod
    def get_base(database_name: str) -> Any:
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_base"):
            raise IndexError(f"Database ({database_name}) has not get_base method. ")

        return database.get_base()

    @staticmethod
    def get_databases() -> List[Database]:
        return list(Persistence.get_instance()._databases.values())

    @staticmethod
    def get_available_databases() -> List[str]:
        return list(Persistence.get_instance()._databases.keys())

    @staticmethod
    def get_available_models_for_database(database_name: str) -> List[str]:
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        return list(database.get_model_names())

    @staticmethod
    def get_model(database_name: str, model_name: str) -> Any:
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")
        return database.get_model(model_name)

    @staticmethod
    def get_session(database_name: str) -> Any:
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_session"):
            raise IndexError(f"Database ({database_name}) has not get_session method. ")

        return database.get_session()

    @staticmethod
    def get_session_scope(database_name: str) -> Callable[..., Any]:
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_session_scope"):
            raise IndexError(
                f"Database ({database_name}) has not get_session_scope method. "
            )

        return database.get_session_scope()
