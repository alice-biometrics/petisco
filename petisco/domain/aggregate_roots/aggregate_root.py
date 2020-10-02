from petisco.domain.base_object import BaseObject
from petisco.event.shared.domain.event import Event, Events


class AggregateRoot(BaseObject):
    def __init__(self):
        self.domain_events: Events = []

    def record(self, event: Event):
        self.domain_events.append(event)

    def clear_domain_events(self):
        self.domain_events = []

    def pull_domain_events(self) -> Events:
        return self.domain_events

    def pull_first_domain_event(self) -> Event:
        return self.domain_events[0] if len(self.domain_events) > 0 else None

    def pull_last_domain_event(self) -> Event:
        return self.domain_events[-1] if len(self.domain_events) > 0 else None
