from __future__ import annotations

import os
from typing import Any, Generic, TypeVar, get_args

from petisco.base.misc.builder import Builder

T = TypeVar("T")


class Dependency(Generic[T]):
    """
    Data structure to define how our dependency (Repository, AppService, etc) is built.

    Definition of default Builder is Mandatory, create alternative builder with envar_modifier is optional.
    """

    # TODO To be deprecated as petisco will index from Generic T by default
    name: str | None = None
    alias: str | None = None  # Use alias instead of name to identify diferent dependencies with the same base type
    default_builder: Builder[T] | None = None
    # TODO, This should be  mandatory (not optional) it is temporary to help on migration to v2
    envar_modifier: str | None = None
    builders: dict[str, Builder[T]] | None = None

    def __init__(
        self,
        name: str | None = None,
        alias: str | None = None,
        default_builder: Builder[Any] | None = None,
        envar_modifier: str | None = None,
        builders: dict[str, Builder[Any]] | None = None,
    ):
        self.name = name
        self.alias = alias
        self.default_builder = default_builder
        self.envar_modifier = envar_modifier
        self.builders = builders

    def _validate(self) -> None:
        generic_type = self.get_generic_type()
        if generic_type:
            if not issubclass(self.default_builder.klass, generic_type):
                raise TypeError(
                    f"Dependency: The class {self.default_builder.klass.__name__} from default_builder is not a subclass from generic type given by Dependency[{generic_type.__name__}]"
                )

            if self.builders is None:
                return

            for key, builder in self.builders.items():
                if not issubclass(builder.klass, generic_type):
                    raise TypeError(
                        f"Dependency: The class {builder.klass.__name__} from builders ({key}) is not a subclass from generic type given by Dependency[{generic_type.__name__}]"
                    )

    def get_generic_type(self) -> type[T] | None:
        """
        Returns type from given generic if exists.
        """
        if not hasattr(self, "__orig_class__"):
            return None
        return get_args(self.__orig_class__)[0]  # type: ignore

    def get_instance(self) -> T:
        """
        Returns an instance of the dependency.
        """

        self._validate()

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
