from petisco import SqlAlchemyPersistenceConfig, SqlAlchemyPersistenceConnector


def config_persistence():

    config = SqlAlchemyPersistenceConfig(server="sqlite", database="petisco.db")
    persistence_connector = SqlAlchemyPersistenceConnector(config=config)
    persistence_connector.execute()
