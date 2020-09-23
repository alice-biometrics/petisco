from typing import Dict, List
from abc import ABCMeta, abstractmethod

from petisco.event.shared.domain.event_subscriber import EventSubscriber


class IEventConsumer:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"IEventConsumer"

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    @abstractmethod
    def consume(self, subscribers: List[EventSubscriber]):
        raise NotImplementedError
