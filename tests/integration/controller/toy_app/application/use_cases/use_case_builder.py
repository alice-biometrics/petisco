from petisco.application.application_config import ApplicationConfig
from tests.integration.controller.toy_app.application.use_cases.create_user import (
    CreateUser,
)
from tests.integration.controller.toy_app.application.use_cases.get_user_name import (
    GetUserName,
)


class UseCaseBuilder:
    @staticmethod
    def create_user():

        config = ApplicationConfig.get_instance()
        repositories = config.repositories_provider()

        return CreateUser(user_repository=repositories["user"])

    @staticmethod
    def get_user_name():
        config = ApplicationConfig.get_instance()
        repositories = config.repositories_provider()

        return GetUserName(user_repository=repositories["user"])
