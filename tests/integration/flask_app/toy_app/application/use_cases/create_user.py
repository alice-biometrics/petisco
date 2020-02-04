from meiga import Result, Success, Error

from petisco import UseCase, use_case_handler, IEventManager
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.name import Name
from petisco.domain.entities.user_id import UserId
from tests.integration.flask_app.toy_app.application_setup import EVENT_TOPIC
from tests.integration.flask_app.toy_app.domain.events.user_created import UserCreated
from tests.integration.flask_app.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class CreateUser(UseCase):
    def __init__(self, user_repository: IUserRepository, event_manager: IEventManager):
        self.user_repository = user_repository
        self.event_manager = event_manager

    def execute(self, client_id: ClientId, name: Name) -> Result[UserId, Error]:
        user_id = UserId.generate().to_result().unwrap_or_return()
        self.user_repository.save(
            client_id=client_id, user_id=user_id, name=name
        ).unwrap_or_return()

        self.event_manager.send(EVENT_TOPIC, UserCreated(user_id))
        return Success(user_id)
