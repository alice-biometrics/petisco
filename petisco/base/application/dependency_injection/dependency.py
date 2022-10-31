import os
from typing import Any, Dict, Union

from petisco.base.misc.builder import Builder


class Dependency:
    name: str
    default_builder: Builder
    envar_modifier: Union[str, None] = None
    builders: Union[Dict[str, Builder], None] = None

    def __init__(
        self,
        name: str,
        default_builder: Builder,
        envar_modifier: Union[str, None] = None,
        builders: Union[Dict[str, Builder], None] = None,
    ):
        self.name = name
        self.default_builder = default_builder
        self.envar_modifier = envar_modifier
        self.builders = builders

    def get_instance(self) -> Any:
        if not self.envar_modifier:
            return self.default_builder.build()

        modifier = os.getenv(self.envar_modifier)
        if not modifier or not self.builders or modifier not in self.builders:
            return self.default_builder.build()
        else:
            builder = self.builders.get(modifier)
            assert isinstance(
                builder, Builder
            ), "Oh no! Dependency builder is corrupted!"
            instance = builder.build()
            return instance
