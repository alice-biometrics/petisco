from typing import Dict

from petisco.events.subscriber.domain.interface_event_subscriber import IEventSubscriber


class NotImplementedEventSubscriber(IEventSubscriber):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def subscribe_all(self):
        pass

    def unsubscribe_all(self):
        pass
