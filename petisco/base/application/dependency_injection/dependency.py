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
    strict: bool = True

    def __init__(
        self,
        type: T | None = None,
        *,
        name: str | None = None,  # to be deleted
        alias: str | None = None,
        default_builder: Builder[Any] | None = None,  # to be deleted
        envar_modifier: str | None = None,
        builders: dict[str, Builder[Any]] | None = None,  # mandatory
        strict: bool = True,
    ):
        self.type = type
        self.name = name
        self.alias = alias
        self.envar_modifier = self._set_envar_modifier(envar_modifier)
        self.default_builder = default_builder
        self.builders = builders
        self.strict = strict
        self._set_default_builders()  # temporary as default_builder is still valid

    def get_key(self) -> str:
        if self.alias:
            return self.alias
        # TODO: to be deleted
        if self.name:
            return self.name
        return self.type

    def _set_default_builders(self):
        if not self.builders:
            if self.default_builder:
                self.builders = {"default": self.default_builder}
        else:
            if self.default_builder:
                self.builders["default"] = self.default_builder

        if self.builders is None or self.builders.get("default") is None:
            raise TypeError(
                f"Dependency: Define a builder for {self.type.__name__} with `default` key. This is mandatory. Given builders={self.builders}"
            )

    def _set_envar_modifier(self, envar_modifier: str | None = None):

        if envar_modifier is None and self.type:
            return (
                # "PETISCO_" + # TODO this will break compatibility (waiting for v2)
                re.sub(r"(?<!^)(?=[A-Z])", "_", self.type.__name__).upper()
                + "_TYPE"
            )

        return envar_modifier

    def _validate(self) -> None:
        if self.type and self.strict:
            if self.builders is None:
                return
            for key, builder in self.builders.items():
                if not issubclass(builder.klass, self.type):
                    raise TypeError(
                        f"Dependency: The class {builder.klass.__name__} from builders ({key}) is not a subclass from "
                        f"generic type given by Dependency[{self.type.__name__}]. If you want to skip it use "
                        f"Dependency(strict=False) "
                    )

    def get_instance(self) -> T:
        """
        Returns an instance of the dependency.
        """

        self._validate()

        modifier = os.getenv(self.envar_modifier) if self.envar_modifier else None
        if not modifier:
            builder = self._get_default_builder()
            instance = builder.build()
            return instance
        else:
            builder = self.builders.get(modifier)
            if not builder:
                builder = self._get_default_builder()
            assert isinstance(
                builder, Builder
            ), "Oh no! Dependency builder is corrupted!"
            instance = builder.build()
            return instance

    def _get_default_builder(self) -> Builder:
        builder = self.builders.get("default")
        if not builder:
            raise TypeError(
                f"Dependency: Define a default builder for {self.type.__name__}. This is mandatory."
            )
        return builder
