from __future__ import annotations

from collections import defaultdict
from typing import Generic, TypeVar

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.misc.singleton import Singleton

T = TypeVar("T")


class Container(Generic[T], metaclass=Singleton):
    """
    Singleton which contains set dependencies (List[Dependency)) prepared to be instantiated in order to be injected
     in the UseCases of our application
    """

    def __init__(self) -> None:
        self.dependencies: dict[str, Dependency] = defaultdict()

    @staticmethod
    def get(base_type: type[T], *, alias: str | None = None) -> T:
        """
        Returns an instance of set Dependency.
        """
        container = Container()

        key = base_type if not alias else alias
        dependency = container.dependencies.get(key)
        if dependency is None:
            key_str = key.__name__ if isinstance(key, type) else key
            raise IndexError(
                f"Invalid dependency. `{key_str}` is not found within available dependencies [{container.get_available_dependencies()}]"
            )
        instance = dependency.get_instance()
        return instance

    @staticmethod
    def set_dependencies(
        dependencies: list[Dependency] | None = None, overwrite: bool = False
    ) -> None:
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
        return [key if isinstance(key, str) else key.__name__ for key in keys]

    def _set_dependencies(
        self, input_dependencies: list[Dependency], overwrite: bool = False
    ) -> None:
        for dependency in input_dependencies:

            if dependency.name:
                if dependency.name in self.dependencies and not overwrite:
                    raise IndexError(
                        f"Container: dependency (name={dependency.name}) is already added to dependencies. Check "
                        f"set_dependencies input "
                    )
                self.dependencies[dependency.name] = dependency
            elif dependency.alias:
                if dependency.alias in self.dependencies and not overwrite:
                    raise IndexError(
                        f"Container: dependency (alias={dependency.alias}) is already added to dependencies. Check "
                        f"set_dependencies input "
                    )
                self.dependencies[dependency.alias] = dependency
            else:
                if dependency.type:
                    if dependency.type in self.dependencies and not overwrite:
                        raise IndexError(
                            f"Container: dependency (type={dependency.type.__name__}) is already added to "
                            f"dependencies. Use Dependency alias to set different dependencies with the same base type "
                        )
                    self.dependencies[dependency.type] = dependency
