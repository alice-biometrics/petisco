from typing import Dict

from petisco.event.bus.domain.interface_event_bus import IEventBus
from petisco.event.shared.domain.event import Event


class NotImplementedEventBus(IEventBus):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def publish(self, event: Event):
        if hasattr(self, "info_id"):
            event = event.add_info_id(self.info_id)

        if hasattr(self, "additional_meta"):
            event = event.update_meta(self.additional_meta)

        if not event or not issubclass(event.__class__, Event):
            raise TypeError("Bus only publishes petisco.Event objects")

    def retry_publish_only_on_store_queue(self, event: Event):
        if not event or not issubclass(event.__class__, Event):
            raise TypeError("Bus only publishes petisco.Event objects")

    def stop(self):
        pass
