from abc import abstractmethod

from meiga import NotImplementedMethodError, Result

from petisco.base.application.patterns.base_pattern import BasePattern


class AppService(BasePattern):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Result:
        return NotImplementedMethodError
