from typing import List

from petisco.events.interface_event_manager import IEventManager
from petisco.events.not_implemented_event_manager import NotImplementedEventManager

EVENT_MANAGER_DEFAULT = NotImplementedEventManager()
EVENT_TOPIC_DEFAULT = "event-topic-undefined"
EVENT_ADDITIONAL_DEFAULT = None


class EventConfig:
    def __init__(
        self,
        event_manager: IEventManager = EVENT_MANAGER_DEFAULT,
        event_topic: str = EVENT_TOPIC_DEFAULT,
        event_additional_info: List[str] = EVENT_ADDITIONAL_DEFAULT,
    ):
        """
        Parameters
        ----------
        event_manager
            A IEventManager implementation. Default NotImplementedEventManager
        event_topic
            Event Topic. By default event-topic-undefined.
        event_additional_info
            A list of additional info to get from function argument and add to RequestResponded Event
        """
        self.event_manager = event_manager
        self.event_topic = event_topic
        self.event_additional_info = event_additional_info
        self.set_is_configured()

    def set_is_configured(self):
        self.is_configured = False
        if (
            not isinstance(self.event_manager, EVENT_MANAGER_DEFAULT.__class__)
            or self.event_topic != EVENT_TOPIC_DEFAULT
            or self.event_additional_info != EVENT_ADDITIONAL_DEFAULT
        ):
            self.is_configured = True

    def get_additional_info(self, kwargs):
        if not self.event_additional_info:
            return None

        additional_info = {}
        for info_key in self.event_additional_info:
            info_value = kwargs.get(info_key)
            if info_value:
                additional_info[info_key] = info_value

        return additional_info
