from typing import List

from petisco.events.interface_event_manager import IEventManager
from petisco.events.not_implemented_event_manager import NotImplementedEventManager


class EventConfig:
    def __init__(
        self,
        event_manager: IEventManager = NotImplementedEventManager(),
        event_topic: str = "petisco",
        event_additional_info: List[str] = None,
    ):
        """
        Parameters
        ----------
        event_manager
            A IEventManager implementation. Default NotImplementedEventManager
        event_topic
            Event Topic. By default petisco.
        event_additional_info
            A list of additional info to get from function argument and add to RequestResponded Event
        """
        self.event_manager = event_manager
        self.event_topic = event_topic
        self.event_additional_info = event_additional_info

    def get_additional_info(self, kwargs):
        if not self.event_additional_info:
            return None

        additional_info = {}
        for info_key in self.event_additional_info:
            info_value = kwargs.get(info_key)
            if info_value:
                additional_info[info_key] = info_value

        return additional_info
