from abc import ABCMeta, abstractmethod
from typing import Dict

from petisco.cqrs.domain.command import Command


class CommandBus:

    __metaclass__ = ABCMeta

    def __init__(self, command_handlers: Dict):
        self.command_handlers = command_handlers

    @abstractmethod
    def dispatch(self, command: Command):
        raise NotImplementedError
