from meiga import Result, Success, Error

from petisco import UseCase, use_case_handler, InfoId
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from petisco.events.publisher.domain.interface_event_publisher import IEventPublisher
from tests.integration.flask_app.toy_app.domain.aggregate_roots.user import User
from tests.integration.flask_app.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class CreateUser(UseCase):
    def __init__(self, user_repository: IUserRepository, publisher: IEventPublisher):
        self.user_repository = user_repository
        self.publisher = publisher

    def execute(self, info_id: InfoId, name: Name) -> Result[UserId, Error]:
        user = User.create(info_id, name)
        self.user_repository.save(user).unwrap_or_return()
        self.publisher.publish_list(user.pull_domain_events())
        return Success(user.user_id)
