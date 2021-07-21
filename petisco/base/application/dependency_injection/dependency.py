import os
from typing import Dict

from petisco.base.misc.builder import Builder


class Dependency:
    name: str
    default_builder: Builder
    envar_modifier: str = None
    builders: Dict[str, Builder] = None

    def __init__(
        self,
        name: str,
        default_builder: Builder,
        envar_modifier: str = None,
        builders: Dict[str, Builder] = None,
    ):
        self.name = name
        self.default_builder = default_builder
        self.envar_modifier = envar_modifier
        self.builders = builders

    def get_instance(self):
        if not self.envar_modifier:
            return self.default_builder.build()

        modifier = os.getenv(self.envar_modifier)
        if not modifier or not self.builders or modifier not in self.builders:
            return self.default_builder.build()
        else:
            instance = self.builders.get(modifier).build()
            return instance
