from meiga import Result, Success, Error

from petisco import UseCase, use_case_handler, InfoId, Petisco
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from petisco.event.legacy.publisher.domain.interface_event_publisher import (
    IEventPublisher,
)
from tests.integration.flask_app.toy_app.domain.aggregate_roots.user import User
from tests.integration.flask_app.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class CreateUser(UseCase):
    @staticmethod
    def build():
        return CreateUser(
            repository=Petisco.get_repository("user"),
            publisher=Petisco.get_event_publisher(),
        )

    def __init__(self, repository: IUserRepository, publisher: IEventPublisher):
        self.repository = repository
        self.publisher = publisher

    def execute(self, info_id: InfoId, name: Name) -> Result[UserId, Error]:
        user = User.create(info_id, name)
        self.repository.save(user).unwrap_or_return()
        self.publisher.publish_events(user.pull_domain_events())
        return Success(user.user_id)
