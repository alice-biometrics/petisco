from abc import ABC, abstractmethod


class ControllerExecutorWrapper(ABC):
    @abstractmethod
    def execute(self, api_controller, *args, **kwargs):
        pass


class DefaultControllerExecutorWrapper(ControllerExecutorWrapper):
    def execute(self, api_controller, *args, **kwargs):
        api_controller._execute_controller(*args, **kwargs)  # noqa
