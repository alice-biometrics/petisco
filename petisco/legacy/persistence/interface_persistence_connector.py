from abc import ABCMeta, abstractmethod

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class IPersistenceConnector:

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        raise NotImplementedError
