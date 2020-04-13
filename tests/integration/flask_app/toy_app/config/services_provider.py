from typing import Dict

from petisco import IService
from tests.integration.flask_app.toy_app.infrastructure.services.sum_service import (
    SumService,
)


def services_provider() -> Dict[str, IService]:
    return {"sum": SumService()}
