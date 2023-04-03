from collections import defaultdict
from typing import Dict, Generic, List, Type, TypeVar, Union

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.misc.singleton import Singleton

T = TypeVar("T")


class Container(Generic[T], metaclass=Singleton):
    """
    Singleton which contains set dependencies (List[Dependency)) prepared to be instantiated in order to be injected
     in the UseCases of our application
    """

    def __init__(self) -> None:
        self.dependencies: Dict[str, Dependency] = defaultdict()

    @staticmethod
    def get(name: Type[T]) -> T:
        """
        Returns an instance of set Dependency.
        """
        container = Container()
        dependency = container.dependencies.get(name)
        if dependency is None:
            raise IndexError(
                f"Invalid dependency. {name} is not found within available dependencies [{container.get_available_dependencies()}]"
            )
        instance = dependency.get_instance()
        return instance

    @staticmethod
    def set_dependencies(
        dependencies: Union[List[Dependency], None] = None, overwrite: bool = True
    ) -> None:
        """
        Set dependencies from a list of them.
        """
        if dependencies is None:
            dependencies = []
        Container()._set_dependencies(dependencies, overwrite)

    @staticmethod
    def get_available_dependencies() -> List[str]:
        """
        Returns the names (keys) of set dependencies.
        """
        return list(Container().dependencies.keys())

    def _set_dependencies(
        self, input_dependencies: List[Dependency], overwrite: bool = True
    ) -> None:
        for dependency in input_dependencies:

            if dependency.name:
                if dependency.name in self.dependencies and not overwrite:
                    raise IndexError(
                        f"Container: dependency (name={dependency.name}) is already added to dependencies. check set_dependencies input"
                    )
                self.dependencies[dependency.name] = dependency
            elif dependency.alias:
                if dependency.alias in self.dependencies and not overwrite:
                    raise IndexError(
                        f"Container: dependency (alias={dependency.alias}) is already added to dependencies. check set_dependencies input"
                    )
                self.dependencies[dependency.alias] = dependency
            else:
                if dependency.type:
                    if dependency.type in self.dependencies and not overwrite:
                        raise IndexError(
                            f"Container: dependency (type={dependency.type.__name__}) is already added to dependencies. Use Dependency alias to set different dependencies with the same base type"
                        )
                    self.dependencies[dependency.type] = dependency
