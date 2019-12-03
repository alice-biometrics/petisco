from petisco.application.application_config import ApplicationConfig
from petisco.events.redis.fake_redis_event_manager import FakeRedisEventManager
from petisco.persistence.sqlalchemy.sqlalchemy_persistence_config import (
    SqlAlchemyPersistenceConfig,
)
from petisco.persistence.sqlalchemy.sqlalchemy_persistence_connector import (
    SqlAlchemyPersistenceConnector,
)
from tests.integration.flask_app.toy_app.application.handlers import redis_event_handler
from tests.integration.flask_app.toy_app.infrastructure.services.sum_service import (
    SumService,
)

AVAILABLE_MODES = {"TEST": ""}

EVENT_TOPIC = "topic"


def repositories_provider():
    from tests.integration.flask_app.toy_app.infrastructure.repositories.sql_user_repository import (
        SqlUserRepository,
    )

    return {"user": SqlUserRepository()}


def services_provider():
    return {"sum": SumService()}


def config_persistence():
    def import_database_models():
        from tests.integration.flask_app.toy_app.infrastructure.repositories.user_model import (
            UserModel,
        )

    config = SqlAlchemyPersistenceConfig(server="sqlite", database="petisco.db")
    persistence_connector = SqlAlchemyPersistenceConnector(
        config=config, import_database_models=import_database_models
    )
    persistence_connector.execute()


REPOSITORIES_MODE_MAPPER = {"TEST": repositories_provider}

SERVICES_MODE_MAPPER = {"TEST": services_provider}


def application_setup():

    event_manager = FakeRedisEventManager(
        subscribers={EVENT_TOPIC: redis_event_handler}
    )

    ApplicationConfig(
        mode="TEST",
        repositories_mode_mapper=REPOSITORIES_MODE_MAPPER,
        services_mode_mapper=SERVICES_MODE_MAPPER,
        event_manager=event_manager,
        config_persistence=config_persistence,
    )
