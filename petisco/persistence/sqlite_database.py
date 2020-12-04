import os
from typing import List

from petisco.persistence.interface_database import IDatabase
from petisco.persistence.persistence_models import PersistenceModels


class SqliteConnection:
    def __init__(self, server_name: str, database_name: str, url: str):
        self.server_name = server_name
        self.database_name = database_name
        self.url = url

    @staticmethod
    def create(server_name: str, database_name: str):
        url = f"{server_name}:///{database_name}"
        return SqliteConnection(server_name, database_name, url)


class SqliteDatabase(IDatabase):
    def __init__(self, name: str, connection: SqliteConnection, model_filename: str):
        if not connection:
            raise ConnectionError("SqliteDatabase needs a valid connection")
        self.persistence_models = PersistenceModels.from_filename(model_filename)
        self.connection = connection
        super().__init__(name)
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

        self.session = sessionmaker(bind=engine)

    def delete(self):
        os.remove(self.connection.database_name)

    def get_base(self):
        return self.base

    def get_model(self, model_name: str):
        model = self.models.get(model_name)
        if not model:
            raise IndexError(
                f'Model "{model_name}" is not available for "{self.name}" database'
            )
        return model

    def get_model_names(self) -> List[str]:
        return list(self.models.keys())
