from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union


class Database(ABC):
    def __init__(self, name: str, models: Union[Dict[str, Any], None] = None):
        self.name = name
        self.models = models if models else {}

    def info(self) -> Dict[str, Any]:
        _info: Dict[str, Any] = {"name": self.name}
        if self.models:
            _info["models"] = self.models
        return _info

    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear_data(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_model(self, model_name: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_model_names(self) -> List[str]:
        raise NotImplementedError
