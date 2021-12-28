from collections import defaultdict
from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.misc.singleton import Singleton


class Container(metaclass=Singleton):
    def __init__(self):
        self.dependencies = defaultdict()

    @staticmethod
    def get(name: str):
        container = Container()
        dependency = container.dependencies.get(name)
        if dependency is None:
            raise IndexError(
                f"Invalid dependency. {name} is not found within available dependencies [{container.get_available_dependencies()}]"
            )
        instance = dependency.get_instance()
        return instance

    @staticmethod
    def set_dependencies(dependencies: List[Dependency] = None):
        if dependencies is None:
            dependencies = []
        Container()._set_dependencies(dependencies)

    @staticmethod
    def get_available_dependencies() -> List[str]:
        return list(Container().dependencies.keys())

    def _set_dependencies(self, input_dependencies: List[Dependency]):
        for dependency in input_dependencies:
            if dependency.name not in self.dependencies:
                self.dependencies[dependency.name] = dependency
