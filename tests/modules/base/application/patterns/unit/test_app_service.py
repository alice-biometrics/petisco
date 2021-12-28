import pytest
from meiga import Result

from petisco import AppService


class TestAppService(AppService):
    def execute(self, *args, **kwargs) -> Result:
        pass


@pytest.mark.unit
def test_app_service_should_construct_an_object():
    app_service = TestAppService()

    assert app_service.info() == {"name": "TestAppService"}


@pytest.mark.unit
def test_app_service_should_overwrite_info_method():
    class NoInfoAppService(TestAppService):
        def info(self):
            return None

    app_service = NoInfoAppService()

    assert app_service.info() is None
