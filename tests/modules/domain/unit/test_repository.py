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


@pytest.mark.unit
def test_should_inherit_from_repository_and_configure_one_with_client_id_getting_client_id():
    class Repository(IRepository):
        pass

    repository = Repository()
    repository_with_client_id = repository.with_client_id(ClientId("acme"))

    client_id = repository_with_client_id.get_client_id()
    assert isinstance(client_id, ClientId)

    client_id_value = repository_with_client_id.get_client_id_value()
    assert isinstance(client_id_value, str)


@pytest.mark.unit
def test_should_inherit_from_repository_and_fail_when_getting_client_id_without_configuring_it():
    class Repository(IRepository):
        pass

    repository = Repository()
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
