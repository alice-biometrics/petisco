from abc import abstractmethod
from typing import NoReturn

from petisco.base.misc.interface import Interface


class ApplicationConfigurer(Interface):
    def __init__(self, execute_after_dependencies: bool = False):
        self.execute_after_dependencies = execute_after_dependencies

    @abstractmethod
    def execute(self, testing: bool = False) -> NoReturn:
        raise NotImplementedError()
