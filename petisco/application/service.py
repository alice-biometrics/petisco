from abc import ABCMeta, abstractmethod
from typing import Dict


class Service:

    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self) -> Dict:
        return {"Service": "Not Implemented"}
