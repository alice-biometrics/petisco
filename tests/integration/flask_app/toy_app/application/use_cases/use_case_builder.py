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
        _, repositories, event_manager = Petisco.providers()
        return CreateUser(
            user_repository=repositories.user, event_manager=event_manager
        )

    @staticmethod
    def get_user_name():
        user_repository = Petisco.repositories().user
        return GetUserName(user_repository=user_repository)
