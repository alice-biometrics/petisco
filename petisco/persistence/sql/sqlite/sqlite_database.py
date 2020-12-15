import os
from typing import List, Callable

from petisco.persistence.interface_database import IDatabase
from petisco.persistence.persistence_models import PersistenceModels
from petisco.persistence.sql.sql_session_scope_provider import (
    sql_session_scope_provider,
)
from petisco.persistence.sql.sqlite.sqlite_connection import SqliteConnection


class SqliteDatabase(IDatabase):
    def __init__(
        self, name: str, connection: SqliteConnection, model_filename: str = None
    ):
        if not connection or not isinstance(connection, SqliteConnection):
            raise ConnectionError(
                "SqliteDatabase needs a valid SqliteConnection connection"
            )
        if model_filename:
            self.persistence_models = PersistenceModels.from_filename(model_filename)
        else:
            self.persistence_models = PersistenceModels(models={})
        self.connection = connection
        super().__init__(name, self.persistence_models.models)
        self._init()

    def _init(self):
        from sqlalchemy.ext.declarative import declarative_base

        self.base = declarative_base()

    def create(self):
        self.persistence_models.import_models()
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy_utils import database_exists, create_database

        engine = create_engine(
            self.connection.url,
            json_serializer=lambda obj: obj,
            json_deserializer=lambda obj: obj,
        )

        if not database_exists(engine.url):
            create_database(engine.url)
            self.base.metadata.create_all(engine)

        self.session_maker = sessionmaker(bind=engine)

    def delete(self):
        if os.path.exists(self.connection.database_name):
            os.remove(self.connection.database_name)

    def get_base(self):
        return self.base

    def get_model(self, model_name: str):
        model = self.persistence_models.get_imported_models().get(model_name)
        if not model:
            raise IndexError(
                f'Model "{model_name}" is not available for "{self.name}" database'
            )
        return model

    def get_model_names(self) -> List[str]:
        return list(self.persistence_models.get_models_names().keys())

    def get_session(self):
        return self.session_maker()

    def get_session_scope(self) -> Callable:
        return sql_session_scope_provider(self.get_session())
