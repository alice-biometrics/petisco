from typing import Callable
from petisco.persistence.interface_persistence_connector import IPersistenceConnector
from petisco.persistence.sqlalchemy.sqlalchemy_persistence import SqlAlchemyPersistence
from petisco.persistence.sqlalchemy.sqlalchemy_persistence_config import (
    SqlAlchemyPersistenceConfig,
)


class SqlAlchemyPersistenceConnector(IPersistenceConnector):
    def __init__(
        self,
        config: SqlAlchemyPersistenceConfig,
        import_database_models: Callable = None,
    ):
        self.config = config
        self.import_database_models = import_database_models

    def get_connection(self):
        connection = None
        if self.config.server:
            if self.config.server == "sqlite":
                connection = "{}:///{}".format(self.config.server, self.config.database)
            elif self.config.server == "mysql":
                connection = "{}+{}://{}:{}@{}:{}/{}".format(
                    self.config.server,
                    self.config.driver,
                    self.config.user,
                    self.config.password,
                    self.config.host,
                    self.config.port,
                    self.config.database,
                )
        return connection

    def execute(self):
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy_utils import database_exists, create_database

        connection = self.get_connection()

        persistence = SqlAlchemyPersistence(base=declarative_base())

        self.import_database_models()

        if not connection:
            raise ConnectionError(
                "Petisco SqlAlchemyPersistenceConnector is not configured. "
                "Please check SqlAlchemyPersistenceConfig and add required values"
            )

        if self.config.server == "sqlite":
            engine = create_engine(
                connection,
                json_serializer=lambda obj: obj,
                json_deserializer=lambda obj: obj,
            )
        else:
            engine = create_engine(
                connection,
                pool_pre_ping=True,
                json_serializer=lambda obj: obj,
                json_deserializer=lambda obj: obj,
            )

        if not database_exists(engine.url):
            create_database(engine.url)
            persistence.base.metadata.create_all(engine)

        persistence.session = sessionmaker(bind=engine)
