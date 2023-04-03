from __future__ import annotations

import os
import re
from typing import Any, Generic, TypedDict, TypeVar

from petisco.base.misc.builder import Builder

T = TypeVar("T")


class Builders(TypedDict):
    key: str
    builder: Builder


class Dependency(Generic[T]):
    """
    Data structure to define how our dependency (Repository, AppService, etc) is built.

    Definition of default Builder is Mandatory, create alternative builder with envar_modifier is optional.
    """

    type: T | None = None
    builders: dict[
        str, Builder[T]
    ] | None = None  # This should be  mandatory (not optional) it is temporary to help on migration to v2
    alias: str | None = None  # Use alias instead of name to identify different dependencies with the same base type
    envar_modifier: str | None = None

    # TODO To be deprecated
    name: str | None = None  # as petisco will index from Generic T by default
    default_builder: Builder[T] | None = None  # as use builders with default value

    def __init__(
        self,
        type: T | None = None,
        *,
        name: str | None = None,  # to be deleted
        alias: str | None = None,
        default_builder: Builder[Any] | None = None,  # to be deleted
        envar_modifier: str | None = None,
        builders: dict[str, Builder[Any]] | None = None,  # mandatory
    ):
        self.type = type
        self.name = name
        self.alias = alias
        self.envar_modifier = self._set_envar_modifier(envar_modifier)
        self.default_builder = default_builder
        self.builders = builders
        self._set_default_builders()  # temporary as default_builder is still valid

    def _set_default_builders(self):
        if not self.builders:
            self.builders = {"default": self.default_builder}
        else:
            self.builders["default"] = self.default_builder

        if self.builders.get("default") is None:
            raise TypeError(
                f"Dependency: Define a builder for {self.type.__name__} with `default` key. This is mandatory."
            )

    def _set_envar_modifier(self, envar_modifier: str | None = None):

        if envar_modifier is None and self.type:
            return re.sub(r"(?<!^)(?=[A-Z])", "_", self.type.__name__).upper() + "_TYPE"

        return envar_modifier

    def _validate(self) -> None:
        if self.type:

            # TODO: simplify as default_builder will be deprecated
            if not issubclass(self.default_builder.klass, self.type):
                raise TypeError(
                    f"Dependency: The class {self.default_builder.klass.__name__} from default_builder is not a subclass from generic type given by Dependency[{self.type.__name__}]"
                )

            if self.builders is None:
                return

            for key, builder in self.builders.items():
                if not issubclass(builder.klass, self.type):
                    raise TypeError(
                        f"Dependency: The class {builder.klass.__name__} from builders ({key}) is not a subclass from generic type given by Dependency[{self.type.__name__}]"
                    )

    def get_instance(self) -> T:
        """
        Returns an instance of the dependency.
        """

        self._validate()

        if not self.envar_modifier:
            builder = self.builders.get("default")
            if not builder:
                raise TypeError(
                    f"Dependency: Define a default builder for {self.type.__name__}. This is mandatory."
                )
            instance = builder.build()
            return instance

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
