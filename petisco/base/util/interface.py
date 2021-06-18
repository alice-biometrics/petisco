from abc import ABC
from typing import Dict


class Interface(ABC):
    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}
