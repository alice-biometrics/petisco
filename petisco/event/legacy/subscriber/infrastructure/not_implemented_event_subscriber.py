from typing import Dict

from petisco.event.legacy.subscriber.domain.interface_event_subscriber import (
    IEventSubscriber,
)


class NotImplementedEventSubscriber(IEventSubscriber):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def start(self):
        pass

    def stop(self):
        pass
