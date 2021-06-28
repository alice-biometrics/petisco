import pytest

from petisco.base.domain.ids.client_id import ClientId
from petisco.base.domain.ids.info_id import InfoId
from petisco.base.domain.ids.user_id import UserId
from petisco.base.application.repository.pattern_base import PatternBase


@pytest.mark.unit
def test_should_inherit_from_pattern_base_and_extend_it_with_client_id():
    class MyRepository(PatternBase):
        pass

    repository = MyRepository()

    client_id = ClientId("client-id")

    repository_with_client_id = repository.with_client_id(client_id)

    assert isinstance(repository_with_client_id, MyRepository)
    assert isinstance(repository_with_client_id.get_client_id(), ClientId)
    assert isinstance(repository_with_client_id.get_client_id_value(), str)
    assert repository_with_client_id.get_client_id() == client_id


@pytest.mark.unit
def test_should_inherit_from_pattern_base_and_extend_it_with_info_id():
    class MyRepository(PatternBase):
        pass

    repository = MyRepository()

    client_id = ClientId("client-id")
    user_id = UserId.v4()
    info_id = InfoId(client_id, user_id)

    repository_with_info_id_id = repository.with_info_id(info_id)

    assert isinstance(repository_with_info_id_id, MyRepository)
    assert isinstance(repository_with_info_id_id.get_client_id(), ClientId)
    assert isinstance(repository_with_info_id_id.get_client_id_value(), str)
    assert repository_with_info_id_id.get_client_id() == client_id
    assert isinstance(repository_with_info_id_id.get_user_id(), UserId)
    assert isinstance(repository_with_info_id_id.get_user_id_value(), str)
    assert repository_with_info_id_id.get_user_id() == user_id
    assert isinstance(repository_with_info_id_id.get_info_id(), InfoId)
    assert repository_with_info_id_id.get_info_id() == info_id
