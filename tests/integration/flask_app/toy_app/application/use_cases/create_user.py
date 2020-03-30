from meiga import Result, Success, Error

from petisco import UseCase, use_case_handler, IEventManager, InfoId
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from tests.integration.flask_app.toy_app.application_setup import EVENT_TOPIC
from tests.integration.flask_app.toy_app.domain.aggregate_roots.user import User
from tests.integration.flask_app.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class CreateUser(UseCase):
    def __init__(self, user_repository: IUserRepository, event_manager: IEventManager):
        self.user_repository = user_repository
        self.event_manager = event_manager

    def execute(self, info_id: InfoId, name: Name) -> Result[UserId, Error]:
        user = User.create(info_id, name)
        self.user_repository.save(user).unwrap_or_return()
        self.event_manager.publish_list(EVENT_TOPIC, user.pull_domain_events())
        return Success(user.user_id)
