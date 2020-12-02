from typing import Dict

from petisco import IApplicationService
from tests.end2end.flask_app.sum.infrastructure.sum_executor import SumExecutor


def services_provider() -> Dict[str, IApplicationService]:
    return {"sum": SumExecutor()}
