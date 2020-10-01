from typing import Dict

from petisco import IRepository
from tests.end2end.flask_app.shared.infrastructure.repositories.sql_user_repository import (
    SqlUserRepository,
)


def repositories_provider() -> Dict[str, IRepository]:
    return {"user": SqlUserRepository.build()}
