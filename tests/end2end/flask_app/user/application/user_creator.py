from meiga import Result, Success, Error

from petisco import UseCase, use_case_handler, InfoId, Petisco
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from petisco.event.bus.domain.interface_event_bus import IEventBus
from petisco.event.legacy.publisher.domain.interface_event_publisher import (
    IEventPublisher,
)
from tests.end2end.flask_app.shared.domain.repositories.interface_user_repository import (
    IUserRepository,
)
from tests.end2end.flask_app.user.domain.aggregate_roots.user import User


@use_case_handler()
class UserCreator(UseCase):
    @staticmethod
    def build():
        return UserCreator(
            repository=Petisco.get_repository("user"),
            publisher=Petisco.get_event_publisher(),
            bus=Petisco.get_event_bus(),
        )

    def __init__(
        self, repository: IUserRepository, publisher: IEventPublisher, bus: IEventBus
    ):
        self.repository = repository
        self.publisher = publisher
        self.bus = bus

    def execute(self, info_id: InfoId, name: Name) -> Result[UserId, Error]:
        user = User.create(info_id, name)
        self.repository.save(user).unwrap_or_return()
        self.publisher.publish_events(user.pull_domain_events())
        self.bus.publish_events(user.pull_domain_events())
        return Success(user.user_id)
