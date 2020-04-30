from typing import Dict

from petisco import IRepository, Petisco
from tests.integration.flask_app.toy_app.infrastructure.repositories.sql_user_repository import (
    SqlUserRepository,
)


def repositories_provider() -> Dict[str, IRepository]:
    return {
        "user": SqlUserRepository(
            session_scope=Petisco.persistence_session_scope(),
            user_model=Petisco.get_persistence_model("user"),
        )
    }
