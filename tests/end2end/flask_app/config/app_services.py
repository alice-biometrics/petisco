from typing import Dict

from petisco import IAppService, AppServices
from tests.end2end.flask_app.sum.infrastructure.sum_executor import SumExecutor


def load_app_services():
    AppServices.load(app_services_provider)


def app_services_provider() -> Dict[str, IAppService]:
    return {"sum": SumExecutor()}
