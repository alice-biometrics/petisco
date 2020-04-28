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
        _, repositories = Petisco.providers()
        return CreateUser(
            user_repository=repositories.user, publisher=Petisco.get_event_publisher()
        )

    @staticmethod
    def get_user_name():
        user_repository = Petisco.repositories().user
        return GetUserName(user_repository=user_repository)
