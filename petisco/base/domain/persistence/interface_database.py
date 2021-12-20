from abc import ABC, abstractmethod
from typing import Dict, List


class Database(ABC):
    def __init__(self, name: str, models: Dict = None):
        self.name = name
        self.models = models if models else {}

    def info(self) -> Dict:
        _info = {"name": self.name}
        if self.models:
            _info["models"] = self.models
        return _info

    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def clear_data(self):
        raise NotImplementedError

    @abstractmethod
    def get_model(self, model_name: str):
        raise NotImplementedError

    @abstractmethod
    def get_model_names(self) -> List[str]:
        raise NotImplementedError
