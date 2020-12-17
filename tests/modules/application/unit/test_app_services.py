from typing import Dict

import pytest

from petisco.application.app_services import AppServices, AppService
from tests.modules.application.mother.app_service_mother import AppServiceMother


@pytest.mark.unit
def test_should_execute_lifecycle_of_app_services_adding_app_service():

    app_services = AppServices()

    app_service = AppServiceMother.valid()

    app_services.add("app_service", app_service)

    assert isinstance(AppServices.get("app_service"), app_service.__class__)
    assert AppServices.info() == {"app_service": {"name": "MyAppService"}}
    AppServices.clear()


@pytest.mark.unit
def test_should_execute_lifecycle_of_app_services_from_provider():

    app_service = AppServiceMother.valid()

    def provider() -> Dict[str, AppService]:
        return {"app_service": app_service}

    AppServices.from_provider(provider)

    assert isinstance(AppServices.get("app_service"), app_service.__class__)
    assert AppServices.info() == {"app_service": {"name": "MyAppService"}}

    AppServices.clear()
