from abc import ABCMeta, abstractmethod
from typing import Dict


class Repository:

    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self) -> Dict:
        return {"Repository": "Not Implemented"}
