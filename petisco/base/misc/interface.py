from abc import ABC
from typing import Any, Dict


class Interface(ABC):
    """
    A base class to Interfaces
    """

    def info(self) -> Dict[str, Any]:
        return {"name": type(self).__name__}
