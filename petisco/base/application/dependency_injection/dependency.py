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

    type: T
    builders: dict[str, Builder[T]]
    alias: str | None = None  # Use alias instead of deprecated name to identify different dependencies with the same base type
    envar_modifier: str | None = None
    strict: bool = True

    def __init__(
        self,
        type: T,  # noqa
        *,
        builders: dict[str, Builder[Any]],
        alias: str | None = None,
        envar_modifier: str | None = None,
        strict: bool = True,
    ):
        self.type = type
        self.alias = alias
        self.envar_modifier = self._set_envar_modifier(envar_modifier)
        self.builders = builders
        self.strict = strict
        self._check()

    def get_key(self) -> str:
        if self.alias:
            return self.alias
        return self.type

    def _check(self):
        if self.builders is None or self.builders.get("default") is None:
            raise TypeError(
                f"Dependency: Define at least one builder for {self.type.__name__} with `default` key. This is "
                f"mandatory. Given builders={self.builders} "
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

                klass = builder.klass
                if hasattr(builder.klass, "__origin__"):
                    klass = builder.klass.__origin__

                if not issubclass(klass, self.type):
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
