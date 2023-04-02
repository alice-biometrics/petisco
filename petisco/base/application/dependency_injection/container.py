from collections import defaultdict
from typing import Dict, Generic, List, TypeVar, Union

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
    def get(name: T) -> T:
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
    def set_dependencies(dependencies: Union[List[Dependency], None] = None) -> None:
        """
        Set dependencies from a list of them.
        """
        if dependencies is None:
            dependencies = []
        Container()._set_dependencies(dependencies)

    @staticmethod
    def get_available_dependencies() -> List[str]:
        """
        Returns the names (keys) of set dependencies.
        """
        return list(Container().dependencies.keys())

    def _set_dependencies(self, input_dependencies: List[Dependency]) -> None:
        for dependency in input_dependencies:

            if dependency.name:
                if dependency.name in self.dependencies:
                    raise IndexError(
                        f"Container: dependency (name={dependency.name}) is already added to dependencies. check set_dependencies input"
                    )
                self.dependencies[dependency.name] = dependency
            elif dependency.alias:
                if dependency.alias in self.dependencies:
                    raise IndexError(
                        f"Container: dependency (alias={dependency.alias}) is already added to dependencies. check set_dependencies input"
                    )
                self.dependencies[dependency.alias] = dependency
            else:
                generic_type = dependency.get_generic_type()
                if generic_type:
                    if generic_type in self.dependencies:
                        raise IndexError(
                            f"Container: dependency (type={generic_type.__name__}) is already added to dependencies. Use Dependency alias to set different dependencies with the same base type"
                        )
                    self.dependencies[generic_type] = dependency
