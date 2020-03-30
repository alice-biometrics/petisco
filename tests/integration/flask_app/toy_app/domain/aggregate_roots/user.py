from petisco import InfoId
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.domain.value_objects.name import Name
from tests.unit.events.test_event import UserCreated


class User(AggregateRoot):
    def __init__(self, info_id: InfoId, name: Name):
        self.info_id = info_id
        self.name = name
        super().__init__()

    @staticmethod
    def create(info_id: InfoId, name: Name):
        user = User(info_id, name)
        user.record(UserCreated(info_id=info_id.to_dict(), name=name))
        return user
