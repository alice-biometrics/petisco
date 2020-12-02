import pytest

from petisco import IApplicationService


@pytest.mark.unit
def test_should_inherit_from_application_service():
    class ApplicationService(IApplicationService):
        pass

    application_service = ApplicationService()

    assert application_service.info() == {"name": "ApplicationService"}


@pytest.mark.unit
def test_should_inherit_from_application_service_and_overwrite_info_method():
    class ApplicationService(IApplicationService):
        def info(self):
            return None

    application_service = ApplicationService()

    assert application_service.info() is None
