import pytest

from petisco import DomainEvent
from petisco.base.domain.ids.info_id import InfoId


class MyAggregateRootCreated(DomainEvent):
    pass


@pytest.mark.unit
def test_info_id_should_success_when_contruct():
    _ = InfoId()
