import pytest

from petisco import IAppService


@pytest.mark.unit
def test_should_inherit_from_application_service():
    class AppService(IAppService):
        pass

    application_service = AppService()

    assert application_service.info() == {"name": "AppService"}


@pytest.mark.unit
def test_should_inherit_from_application_service_and_overwrite_info_method():
    class AppService(IAppService):
        def info(self):
            return None

    application_service = AppService()

    assert application_service.info() is None
