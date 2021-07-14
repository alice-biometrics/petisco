import pytest
from meiga import Result

from petisco.base.application.patterns.repository import Repository
from tests.modules.base.mothers.info_id_mother import InfoIdMother


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


@pytest.mark.unit
def test_repository_should_configure_one_object_with_info_id():
    repository = TestRepository()

    assert not hasattr(repository, "info_id")

    repository_with_info_id = repository.with_info_id(InfoIdMother.any())

    assert hasattr(repository_with_info_id, "info_id")
    assert repository_with_info_id is not repository


@pytest.mark.unit
def test_repository_should_raise_an_exeception_when_getting_info_id_without_configuring_it():
    repository = TestRepository()
    with pytest.raises(AttributeError) as excinfo:
        _ = repository.get_info_id()
    assert (
        "TestRepository needs info_id configuration. Please, use TestRepository.info_id() to get a valid object with info_id"
        in str(excinfo.value)
    )
