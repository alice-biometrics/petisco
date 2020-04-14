from meiga import Result, Success, Error

from petisco import UseCase, use_case_handler, IEventManager, InfoId, Petisco
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
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
        self.event_manager.publish_list(
            Petisco.get_instance().event_topic, user.pull_domain_events()
        )
        return Success(user.user_id)
