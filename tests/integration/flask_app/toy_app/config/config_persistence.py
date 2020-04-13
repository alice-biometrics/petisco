from petisco import SqlAlchemyPersistenceConfig, SqlAlchemyPersistenceConnector


def config_persistence():
    def import_database_models():
        pass

    config = SqlAlchemyPersistenceConfig(server="sqlite", database="petisco.db")
    persistence_connector = SqlAlchemyPersistenceConnector(
        config=config, import_database_models=import_database_models
    )
    persistence_connector.execute()
