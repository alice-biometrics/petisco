import inspect
from typing import List, Callable
from dataclasses import dataclass
from petisco.application.singleton import Singleton
from petisco.persistence.interface_database import IDatabase


@dataclass
class Persistence(metaclass=Singleton):
    def __init__(self):
        self._databases = {}

    def __repr__(self):
        return f"Persistence: {str(self.get_info())}"

    def get_info(self):
        return {name: database.info() for name, database in self._databases.items()}

    @staticmethod
    def info():
        return Persistence.get_instance().get_info()

    @staticmethod
    def get_instance():
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

    def add(self, database: IDatabase):
        if database.name in self._databases:
            raise NameError(f"Database {database.name} is already added to Persistence")
        self._databases[database.name] = database

    def remove(self, database_name: str):
        if database_name in self._databases:
            self._databases[database_name].delete()
            del self._databases[database_name]
        else:
            raise IndexError(
                f"Database name cannot be removed. {database_name} not exists"
            )

    def create(self):
        for database in self._databases.values():
            database.create()

    def delete(self):
        for database in self._databases.values():
            database.delete()

    @staticmethod
    def get_base(database_name: str) -> List[str]:
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_base"):
            raise IndexError(f"Database ({database_name}) has not get_base method. ")

        return database.get_base()

    @staticmethod
    def get_databases() -> List[IDatabase]:
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
    def get_model(database_name: str, model_name: str):
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")
        return database.get_model(model_name)

    @staticmethod
    def get_session(database_name: str):
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_session"):
            raise IndexError(f"Database ({database_name}) has not get_session method. ")

        return database.get_session()

    @staticmethod
    def get_session_scope(database_name: str) -> Callable:
        database = Persistence.get_instance()._databases.get(database_name)
        if not database:
            raise IndexError(f"Database name ({database_name}) not exists.")

        if not hasattr(database, "get_session_scope"):
            raise IndexError(
                f"Database ({database_name}) has not get_session_scope method. "
            )

        return database.get_session_scope()
