import pytest

from petisco import IRepository, ClientId


@pytest.mark.unit
def test_should_inherit_from_repository():
    class Repository(IRepository):
        pass

    repository = Repository()

    assert repository.info() == {"name": "Repository"}


@pytest.mark.unit
def test_should_inherit_from_repository_and_overwrite_info_method():
    class Repository(IRepository):
        def info(self):
            return None

    repository = Repository()

    assert repository.info() is None


@pytest.mark.unit
def test_should_inherit_from_repository_and_configure_one_with_client_id():
    class Repository(IRepository):
        pass

    repository = Repository()

    assert not hasattr(repository, "client_id")

    repository_with_client_id = repository.with_client_id(ClientId("acme"))

    assert hasattr(repository_with_client_id, "client_id")
    assert repository_with_client_id is not repository
