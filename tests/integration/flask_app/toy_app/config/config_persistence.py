from typing import Callable
from petisco import SqlAlchemyPersistenceConfig, SqlAlchemyPersistenceConnector


def config_persistence(import_database_models: Callable):

    config = SqlAlchemyPersistenceConfig(server="sqlite", database="petisco.db")
    persistence_connector = SqlAlchemyPersistenceConnector(
        config=config, import_database_models=import_database_models
    )

    persistence_connector.execute()
