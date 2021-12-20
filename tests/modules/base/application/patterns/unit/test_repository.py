import pytest
from meiga import Result

from petisco.base.application.patterns.repository import Repository


class TestRepository(Repository):
    def save(self, *args, **kwargs) -> Result:
        pass

    def retrieve(self, *args, **kwargs) -> Result:
        pass

    def retrieve_all(self, *args, **kwargs) -> Result:
        pass

    def remove(self, *args, **kwargs) -> Result:
        pass


@pytest.mark.unit
def test_repository_should_construct_an_object():
    repository = TestRepository()

    assert repository.info() == {"name": "TestRepository"}


@pytest.mark.unit
def test_repository_should_overwrite_info_method():
    class NoInfoRepository(TestRepository):
        def info(self):
            return None

    repository = NoInfoRepository()

    assert repository.info() is None
