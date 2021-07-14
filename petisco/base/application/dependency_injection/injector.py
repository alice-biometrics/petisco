from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.misc.singleton import Singleton


class Injector(metaclass=Singleton):
    """@DynamicAttrs"""

    def __init__(self):
        self.available_dependencies = []

    @staticmethod
    def get(name: str):
        injector = Injector()
        if not hasattr(injector, name):
            raise IndexError(
                f"Invalid dependency. {name} is not found within available dependencies [{injector.get_available_dependencies()}]"
            )
        return getattr(injector, name)

    @staticmethod
    def set_dependencies(dependencies: List[Dependency] = []):
        Injector()._set_dependencies(dependencies)

    @staticmethod
    def get_available_dependencies() -> List[str]:
        return Injector().available_dependencies

    def _set_dependencies(self, dependencies: List[Dependency] = []) -> List[str]:
        for dependency in dependencies:
            setattr(self, dependency.name, dependency.get_instance())
            if dependency.name not in self.available_dependencies:
                self.available_dependencies.append(dependency.name)
