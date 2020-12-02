from typing import Dict

from petisco import IAppService
from tests.end2end.flask_app.sum.infrastructure.sum_executor import SumExecutor


def services_provider() -> Dict[str, IAppService]:
    return {"sum": SumExecutor()}
