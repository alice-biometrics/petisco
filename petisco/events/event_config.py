from typing import List

from petisco.events.publisher.domain.interface_event_publisher import IEventPublisher
from petisco.events.publisher.infrastructure.not_implemented_event_publisher import (
    NotImplementedEventPublisher,
)

EVENT_PUBLISHER_DEFAULT = NotImplementedEventPublisher()
EVENT_ADDITIONAL_DEFAULT = None


class EventConfig:
    def __init__(
        self,
        publisher: IEventPublisher = EVENT_PUBLISHER_DEFAULT,
        additional_info: List[str] = EVENT_ADDITIONAL_DEFAULT,
    ):
        """
        Parameters
        ----------
        publisher
            A IEventPublisher implementation. Default NotImplementedEventManager
        additional_info
            A list of additional info to get from function argument and add to RequestResponded Event
        """
        self.publisher = publisher
        self.additional_info = additional_info
        self.set_is_configured()

    def set_is_configured(self):
        self.is_configured = False
        if (
            not isinstance(self.publisher, EVENT_PUBLISHER_DEFAULT.__class__)
            or self.additional_info != EVENT_ADDITIONAL_DEFAULT
        ):
            self.is_configured = True

    def get_additional_info(self, kwargs):
        if not self.additional_info:
            return None

        additional_info = {}
        for info_key in self.additional_info:
            info_value = kwargs.get(info_key)
            if info_value:
                additional_info[info_key] = info_value

        return additional_info
