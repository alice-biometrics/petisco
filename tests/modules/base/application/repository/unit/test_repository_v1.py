import pytest
from meiga import Result

from petisco.base.domain.ids.client_id import ClientId
from petisco.base.application.repository.interface_repository import Repository


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
def test_should_inherit_from_repository():
    repository = TestRepository()

    assert repository.info() == {"name": "TestRepository"}


@pytest.mark.unit
def test_should_inherit_from_repository_and_overwrite_info_method():
    class NoInfoRepository(TestRepository):
        def info(self):
            return None

    repository = NoInfoRepository()

    assert repository.info() is None


@pytest.mark.unit
def test_should_inherit_from_repository_and_configure_one_with_client_id():
    repository = TestRepository()

    assert not hasattr(repository, "client_id")

    repository_with_client_id = repository.with_client_id(ClientId("acme"))

    assert hasattr(repository_with_client_id, "client_id")
    assert repository_with_client_id is not repository


@pytest.mark.unit
def test_should_inherit_from_repository_and_configure_one_with_client_id_getting_client_id():
    repository = TestRepository()
    repository_with_client_id = repository.with_client_id(ClientId("acme"))

    client_id = repository_with_client_id.get_client_id()
    assert isinstance(client_id, ClientId)

    client_id_value = repository_with_client_id.get_client_id_value()
    assert isinstance(client_id_value, str)


@pytest.mark.unit
def test_should_inherit_from_repository_and_fail_when_getting_client_id_without_configuring_it():
    repository = TestRepository()
    with pytest.raises(AttributeError) as excinfo:
        _ = repository.get_client_id()
        assert (
            "Repository needs client_id. Please, Repository.use with_client_id() to get a valid"
            in str(excinfo.value)
        )

    with pytest.raises(AttributeError) as excinfo:
        _ = repository.get_client_id_value()
        assert (
            "Repository needs client_id. Please, Repository.use with_client_id() to get a valid"
            in str(excinfo.value)
        )
