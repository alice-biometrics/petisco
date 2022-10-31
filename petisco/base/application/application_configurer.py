from abc import abstractmethod

from petisco.base.misc.interface import Interface


class ApplicationConfigurer(Interface):
    def __init__(self, execute_after_dependencies: bool = False) -> None:
        self.execute_after_dependencies = execute_after_dependencies

    @abstractmethod
    def execute(self, testing: bool = False) -> None:
        raise NotImplementedError()
