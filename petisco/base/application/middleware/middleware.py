from abc import ABC, abstractmethod

from meiga import Result


class Middleware(ABC):
    def __init__(self, wrapped_class_name, wrapped_class_input_arguments):
        self.wrapped_class_name = wrapped_class_name
        self.wrapped_class_input_arguments = wrapped_class_input_arguments

    @abstractmethod
    def before(self):
        pass

    @abstractmethod
    def after(self, result: Result):
        pass
