from typing import Dict

from petisco.event.bus.domain.interface_event_bus import IEventBus
from petisco.event.shared.domain.event import Event


class NotImplementedEventBus(IEventBus):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def publish(self, event: Event):
        pass

    def retry_publish_only_on_store_queue(self, event: Event):
        pass

    def stop(self):
        pass
