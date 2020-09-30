import pytest

from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from petisco.event.shared.domain.event import Event


class UserCreated(Event):
    user_id: UserId
    name: Name

    def __init__(self, user_id: UserId, name: Name):
        self.user_id = user_id
        self.name = name
        super().__init__()


class User(AggregateRoot):
    def __init__(self, name: Name, user_id: UserId):
        self.name = name
        self.user_id = user_id
        super().__init__()

    @staticmethod
    def create(name: Name):
        user = User(name, UserId.generate())
        user.record(UserCreated(user.user_id, user.name))
        return user


@pytest.mark.unit
def test_should_play_with_player_aggregate_root():

    user = User.create(Name("Petisco"))

    assert isinstance(user.pull_first_domain_event(), UserCreated)
    assert isinstance(user.pull_last_domain_event(), UserCreated)
    assert len(user.pull_domain_events()) == 1

    user.clear_domain_events()

    assert user.pull_first_domain_event() is None
    assert user.pull_last_domain_event() is None
    assert len(user.pull_domain_events()) == 0
