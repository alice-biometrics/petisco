from meiga import Result, Success, Error

from petisco import UseCase, use_case_handler, InfoId, Petisco, Repositories
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from petisco.event.bus.domain.interface_event_bus import IEventBus
from tests.end2end.flask_app.shared.domain.repositories.interface_user_repository import (
    IUserRepository,
)
from tests.end2end.flask_app.user.domain.aggregate_roots.user import User


@use_case_handler()
class UserCreator(UseCase):
    @staticmethod
    def build():
        return UserCreator(
            repository=Repositories.get("user"), bus=Petisco.get_event_bus()
        )

    def __init__(self, repository: IUserRepository, bus: IEventBus):
        self.repository = repository
        self.bus = bus

    def execute(self, info_id: InfoId, name: Name) -> Result[UserId, Error]:
        user = User.create(info_id, name)
        self.repository.save(user).unwrap_or_return()
        self.bus.publish_events(user.pull_domain_events())
        return Success(user.user_id)
