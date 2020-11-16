import pytest

from petisco import IService


@pytest.mark.unit
def test_should_inherit_from_service():
    class Service(IService):
        pass

    service = Service()

    assert service.info() == {"name": "Service"}


@pytest.mark.unit
def test_should_inherit_from_service_and_overwrite_info_method():
    class Service(IService):
        def info(self):
            return None

    service = Service()

    assert service.info() is None
