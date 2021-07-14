import pytest

from petisco.base.application.patterns.base_pattern import BasePattern
from petisco.base.domain.ids.info_id import InfoId
from tests.modules.base.mothers.info_id_mother import InfoIdMother


@pytest.mark.unit
def test_base_pattern_should_extend_it_with_info_id():
    class MyRepository(BasePattern):
        pass

    repository = MyRepository()

    info_id = InfoIdMother.any()

    repository_with_info_id = repository.with_info_id(info_id)

    assert isinstance(repository_with_info_id, MyRepository)
    assert isinstance(repository_with_info_id.get_info_id(), InfoId)
    assert isinstance(repository_with_info_id.get_info_id().client_id.value, str)
    assert repository_with_info_id.get_info_id() == info_id


@pytest.mark.unit
def test_base_pattern_should_extend_it_with_redefined_info_id():
    class MyRepository(BasePattern):
        pass

    repository = MyRepository()

    info_id = InfoIdMother.with_redefined_user_id()

    repository_with_info_id = repository.with_info_id(info_id)

    assert isinstance(repository_with_info_id, MyRepository)
    assert isinstance(repository_with_info_id.get_info_id().client_id.value, str)
    assert repository_with_info_id.get_info_id() == info_id
