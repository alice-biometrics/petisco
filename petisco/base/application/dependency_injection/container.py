from __future__ import annotations

from abc import ABC
from collections import defaultdict
from typing import Any, TypeVar

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.misc.singleton import Singleton

T = TypeVar("T", bound=ABC)


class Container(metaclass=Singleton):
    """
    Singleton which contains set dependencies (List[Dependency)) prepared to
    be instantiated in order to be injected in the UseCases of our application
    """

    def __init__(self) -> None:
        self.dependencies: dict[str, Dependency[Any]] = defaultdict()

    @staticmethod
    def get(base_type: type[T], *, alias: str | None = None) -> T:
        """
        Returns an instance of set Dependency.
        """

        container = Container()

        key = base_type.__name__ if not alias else f'{base_type.__name__} (alias="{alias}")'
        dependency = container.dependencies.get(key)
        if dependency is None:
            raise IndexError(
                f"Invalid dependency. `{key}` is not found within available dependencies [{container.get_available_dependencies()}]"
            )
        instance = dependency.get_instance()
        return instance

    @staticmethod
    def set_dependencies(dependencies: list[Dependency[Any]] | None = None, overwrite: bool = False) -> None:
        """
        Set dependencies from a list of them.
        """
        if dependencies is None:
            dependencies = []
        Container()._set_dependencies(dependencies, overwrite)

    @staticmethod
    def get_available_dependencies() -> list[str]:
        """
        Returns the names (keys) of set dependencies.
        """
        keys = list(Container().dependencies.keys())
        return keys

    def _set_dependencies(self, input_dependencies: list[Dependency[Any]], overwrite: bool = False) -> None:
        for dependency in input_dependencies:
            key = dependency.get_key()

            if key in self.dependencies and not overwrite:
                if dependency.alias:
                    raise IndexError(
                        f"Container: dependency ({dependency.type.__name__} with alias={dependency.alias}) is already added to dependencies. Check "
                        f"set_dependencies input "
                    )
                else:
                    raise IndexError(
                        f"Container: dependency (type={dependency.type.__name__}) is already added to "
                        f"dependencies. Use Dependency alias to set different dependencies with the same base type "
                    )

            self.dependencies[key] = dependency
