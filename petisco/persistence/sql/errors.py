from meiga import Error

from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.uuid import Uuid


class ClientNotFoundError(Error):
    def __init__(self, client_id: ClientId):
        self.message = f"{self.__class__.__name__} [client_id: {client_id.value}]"


class ClientAlreadyExistError(Error):
    def __init__(self, client_id: ClientId):
        self.message = f"{self.__class__.__name__} [client_id: {client_id.value}]"


class UserNotFoundError(Error):
    def __init__(self, user_id: UserId):
        self.message = f"{self.__class__.__name__} [user_id: {user_id.value}]"


class UserAlreadyExistError(Error):
    def __init__(self, user_id: UserId):
        self.message = f"{self.__class__.__name__} [user_id: {user_id.value}]"


class EntityAlreadyExistError(Error):
    def __init__(self, repository_name: str, table_name: str, entity_id: Uuid):
        self.message = f"[Repository: {repository_name} | Table: {table_name} | entity_id: {entity_id.value}]"


class EntityNotFoundError(Error):
    def __init__(self, repository_name: str, entity_id: Uuid):
        self.message = f"[Repository: {repository_name} | entity_id: {entity_id.value}]"


class EntitiesNotFoundError(Error):
    def __init__(self, repository_name: str):
        self.message = f"[Repository: {repository_name}]"
