import os
from typing import Callable

from petisco import SqlAlchemyPersistenceConfig, SqlAlchemyPersistenceConnector


def config_persistence(import_database_models: Callable):
    config = SqlAlchemyPersistenceConfig(
        server=os.environ.get("SQL_SERVER"), database=os.environ.get("SQL_DATABASE")
    )
    persistence_connector = SqlAlchemyPersistenceConnector(
        config=config, name="petisco", import_database_models=import_database_models
    )
    persistence_connector.execute()
