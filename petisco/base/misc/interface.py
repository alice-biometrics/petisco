from abc import ABC
from typing import Any, Dict


class Interface(ABC):
    def info(self) -> Dict[str, Any]:
        return {"name": type(self).__name__}
