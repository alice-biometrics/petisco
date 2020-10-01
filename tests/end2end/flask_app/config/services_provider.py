from typing import Dict

from petisco import IService
from tests.end2end.flask_app.sum.infrastructure.sum_executor import SumExecutor


def services_provider() -> Dict[str, IService]:
    return {"sum": SumExecutor()}
