from typing import Dict
from abc import ABCMeta, abstractmethod

from petisco.events.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)


class IEventSubscriber:

    __metaclass__ = ABCMeta

    def __init__(self, subscribers: Dict[str, ConfigEventSubscriber]):
        self.subscribers = subscribers

    def __repr__(self):
        return f"IEventPublisher: [subscribers: {self.subscribers}]"

    @abstractmethod
    def info(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
