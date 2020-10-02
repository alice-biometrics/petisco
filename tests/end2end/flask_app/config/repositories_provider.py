from typing import Dict

from petisco import IRepository
from tests.end2end.flask_app.shared.infrastructure.repositories.sql_user_repository import (
    SqlUserRepository,
)
from tests.end2end.flask_app.users_count.infrastructure.sql_users_count_repository import (
    SqlUsersCountRepository,
)


def repositories_provider() -> Dict[str, IRepository]:
    return {
        "user": SqlUserRepository.build(),
        "users_count": SqlUsersCountRepository.build(),
    }
