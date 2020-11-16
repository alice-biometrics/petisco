from abc import ABCMeta, abstractmethod
from typing import Dict

from meiga import Result, NotImplementedMethodError

from petisco.domain.value_objects.client_id import ClientId
import copy


class IRepository:

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

    @abstractmethod
    def save(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def retrieve_all(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError

    @abstractmethod
    def remove(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError
