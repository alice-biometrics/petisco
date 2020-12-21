from typing import Dict

from petisco import IRepository, Repositories
from tests.end2end.flask_app.shared.infrastructure.repositories.mongodb_user_repository import (
    MongoDBUserRepository,
)
from tests.end2end.flask_app.shared.infrastructure.repositories.sql_user_repository import (
    SqlUserRepository,
)
from tests.end2end.flask_app.users_count.infrastructure.inmemory_users_count_repository import (
    InMemoryUsersCountRepository,
)
from tests.end2end.flask_app.users_count.infrastructure.sql_users_count_repository import (
    SqlUsersCountRepository,
)


def load_repositories(with_mongo: bool = False):
    if with_mongo:
        Repositories.load(repositories_provider_mongo)
    else:
        Repositories.load(repositories_provider)


def repositories_provider() -> Dict[str, IRepository]:
    return {
        "user": SqlUserRepository.build(),
        "users_count": SqlUsersCountRepository.build(),
    }


def repositories_provider_mongo() -> Dict[str, IRepository]:
    return {
        "user": MongoDBUserRepository.build(),
        "users_count": InMemoryUsersCountRepository(),
    }
