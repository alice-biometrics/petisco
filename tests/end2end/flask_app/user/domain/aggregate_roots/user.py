from petisco import InfoId, ClientId, UserId
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.domain.value_objects.name import Name
from tests.end2end.flask_app.user.domain.events.user_created import UserCreated


class User(AggregateRoot):
    def __init__(self, name: Name, client_id: ClientId, user_id: UserId):
        self.client_id = client_id
        self.user_id = user_id
        self.name = name
        super().__init__()

    @staticmethod
    def create(info_id: InfoId, name: Name):
        user = User(name, info_id.client_id, info_id.user_id)
        user_created = UserCreated(name).add_info_id(info_id)
        user.record(user_created)
        return user

    def to_dict(self):
        return {
            "user_id": self.user_id.value,
            "client_id": self.client_id.value,
            "name": self.name.value,
        }
