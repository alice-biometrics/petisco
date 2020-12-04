from abc import ABCMeta, abstractmethod
from typing import List, Dict


class IDatabase:

    __metaclass__ = ABCMeta

    def __init__(self, name: str, models: Dict = None):
        self.name = name
        self.models = models if models else {}

    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def get_model(self, model_name: str):
        raise NotImplementedError

    @abstractmethod
    def get_model_names(self) -> List[str]:
        raise NotImplementedError
