from petisco import InfoId, ClientId, UserId
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.domain.value_objects.name import Name
from tests.unit.events.test_event import UserCreated


class User(AggregateRoot):
    def __init__(self, name: Name, client_id: ClientId, user_id: UserId):
        self.client_id = client_id
        self.user_id = user_id
        self.name = name
        super().__init__()

    @staticmethod
    def create(info_id: InfoId, name: Name):
        user = User(name, info_id.client_id, info_id.user_id)
        user.record(UserCreated(info_id=info_id.to_dict(), name=name))
        return user