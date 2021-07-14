import pytest
from meiga import Result

from petisco import AppService
from tests.modules.base.mothers.info_id_mother import InfoIdMother


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


@pytest.mark.unit
def test_app_service_should_configure_one_object_with_info_id():
    app_service = TestAppService()

    assert not hasattr(app_service, "info_id")

    app_service_with_info_id = app_service.with_info_id(InfoIdMother.any())

    assert hasattr(app_service_with_info_id, "info_id")
    assert app_service_with_info_id is not app_service


@pytest.mark.unit
def test_app_service_should_raise_an_exeception_when_getting_info_id_without_configuring_it():
    app_service = TestAppService()
    with pytest.raises(AttributeError) as excinfo:
        _ = app_service.get_info_id()
    assert (
        "TestAppService needs info_id configuration. Please, use TestAppService.info_id() to get a valid object with info_id"
        in str(excinfo.value)
    )
