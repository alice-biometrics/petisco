from abc import ABC
from typing import Any, Dict


class Interface(ABC):
    @classmethod
    def info(cls) -> Dict[str, Any]:
        return {"name": cls.__name__}
