from abc import ABC, abstractmethod
from typing import Any, Type

from meiga import Error, NotImplementedMethodError, Result


class Transformer(ABC):
    def __init__(self, infrastructure_model: Type):
        self.InfrastructureModel = infrastructure_model

    @abstractmethod
    def get_domain_model(self, infrastructure_model: Any) -> Result[Any, Error]:
        return NotImplementedMethodError

    @abstractmethod
    def get_infrastructure_model(self, domain_model: Any) -> Result[Any, Error]:
        return NotImplementedMethodError
