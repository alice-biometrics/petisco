from petisco import Petisco
from tests.integration.flask_app.toy_app.application.use_cases.create_user import (
    CreateUser,
)
from tests.integration.flask_app.toy_app.application.use_cases.get_user_name import (
    GetUserName,
)


class UseCaseBuilder:
    @staticmethod
    def create_user():
        petisco = Petisco.get_instance()
        user_repository = petisco.repositories_provider()["user"]
        event_manager = petisco.event_manager_provider()

        return CreateUser(user_repository=user_repository, event_manager=event_manager)

    @staticmethod
    def get_user_name():
        petisco = Petisco.get_instance()
        user_repository = petisco.repositories_provider()["user"]

        return GetUserName(user_repository=user_repository)
