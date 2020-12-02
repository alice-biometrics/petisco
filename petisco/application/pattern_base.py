from abc import ABCMeta
from typing import Dict

from petisco.domain.value_objects.client_id import ClientId
import copy


class PatternBase:

    __metaclass__ = ABCMeta

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    def _set_client_id(self, client_id: ClientId):
        self.client_id = client_id

    def with_client_id(self, client_id: ClientId):
        repository = copy.copy(self)
        repository._set_client_id(client_id)
        return repository

    def get_client_id(self) -> ClientId:
        if not hasattr(self, "client_id"):
            name = self.info().get("name")
            raise AttributeError(
                f"{name} needs client_id. Please, {name}.use with_client_id() to get a valid"
            )
        return self.client_id

    def get_client_id_value(self) -> str:
        client_id = self.get_client_id()
        return client_id.value
