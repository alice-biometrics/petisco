from petisco import CorrelationId
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from tests.unit.events.test_event import UserCreated


class User(AggregateRoot):
    def __init__(self, name: Name, client_id: ClientId, user_id: UserId):
        self.name = name
        self.client_id = client_id
        self.user_id = user_id
        super().__init__()

    @staticmethod
    def create(name: Name, client_id: ClientId, correlation_id: CorrelationId = None):
        user = User(name, client_id, UserId.generate())

        user.record(UserCreated(user.user_id, user.client_id, correlation_id))

        return user
