from typing import Dict

from petisco import IRepository


def repositories_provider() -> Dict[str, IRepository]:
    from tests.integration.flask_app.toy_app.infrastructure.repositories.sql_user_repository import (
        SqlUserRepository,
    )

    return {"user": SqlUserRepository()}
