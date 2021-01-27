from abc import ABCMeta
from typing import Dict

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.value_objects.client_id import ClientId
import copy

from petisco.domain.value_objects.user_id import UserId


class PatternBase:

    __metaclass__ = ABCMeta

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    def _set_client_id(self, client_id: ClientId):
        if client_id is not None:
            self.client_id = client_id

    def _set_user_id(self, user_id: UserId):
        if user_id is not None:
            self.user_id = user_id

    def _set_info_id(self, info_id: InfoId):
        self._set_client_id(info_id.client_id)
        self._set_user_id(info_id.user_id)
        self.info_id = info_id

    def with_client_id(self, client_id: ClientId):
        repository = copy.copy(self)
        repository._set_client_id(client_id)
        return repository

    def with_info_id(self, info_id: InfoId):
        repository = copy.copy(self)
        repository._set_info_id(info_id)
        return repository

    def get_client_id(self) -> ClientId:
        if not hasattr(self, "client_id"):
            name = self.info().get("name")
            raise AttributeError(
                f"{name} needs client_id. Please, use {name}.with_client_id() to get a valid object with a client_id"
            )
        return self.client_id

    def get_client_id_value(self) -> str:
        return self.get_client_id().value

    def get_user_id(self) -> UserId:
        if not hasattr(self, "user_id"):
            name = self.info().get("name")
            raise AttributeError(
                f"{name} needs user_id. Please, use {name}.with_info_id() to get a valid with a info_id (client_id and user_id)"
            )
        return self.user_id

    def get_user_id_value(self) -> str:
        return self.get_user_id().value

    def get_info_id(self) -> InfoId:
        if not hasattr(self, "info_id"):
            name = self.info().get("name")
            raise AttributeError(
                f"{name} needs info_id. Please, use {name}.with_info_id() to get a valid with a info_id"
            )
        return self.info_id
