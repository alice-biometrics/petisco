from typing import Dict, Callable
from abc import ABCMeta, abstractmethod

from petisco.events.event import Event


class IEventManager:

    __metaclass__ = ABCMeta

    def __init__(self, subscribers: Dict[str, Callable]):
        self.subscribers = subscribers

    def __repr__(self):
        return f"EventManager: [subscribers: {self.subscribers}]"

    @abstractmethod
    def info(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe_all(self):
        raise NotImplementedError

    @abstractmethod
    def send(self, topic: str, event: Event):
        raise NotImplementedError
