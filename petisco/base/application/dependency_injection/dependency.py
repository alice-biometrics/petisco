import os
from typing import Any, Dict

from pydantic.main import BaseModel


class Dependency(BaseModel):
    name: str
    default_instance: Any
    envar_modifier: str = None
    instances: Dict[str, Any] = None

    def get_instance(self):
        if not self.envar_modifier:
            return self.default_instance

        modifier = os.getenv(self.envar_modifier)
        if not modifier or modifier not in self.instances:
            return self.default_instance
        else:
            instance = self.instances.get(modifier)
            return instance
