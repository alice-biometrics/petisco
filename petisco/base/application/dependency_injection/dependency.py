import os
from typing import Dict, Generic, TypeVar, Union

from petisco.base.misc.builder import Builder

TD = TypeVar("TD")
TA = TypeVar("TA")


class Dependency(Generic[TD, TA]):
    name: str
    default_builder: Builder[TD]
    envar_modifier: Union[str, None] = None
    builders: Union[Dict[str, Builder[TA]], None] = None

    def __init__(
        self,
        name: str,
        default_builder: Builder[TD],
        envar_modifier: Union[str, None] = None,
        builders: Union[Dict[str, Builder[TA]], None] = None,
    ):
        self.name = name
        self.default_builder = default_builder
        self.envar_modifier = envar_modifier
        self.builders = builders

    def get_instance(self) -> Union[TD, TA]:
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
