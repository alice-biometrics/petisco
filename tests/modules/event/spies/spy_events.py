from petisco import Event, EventId


class SpyEvents:
    def __init__(self):
        self.counter_events = {}
        self.events = []

    def __repr__(self):
        return f"SpyEvents: {self.events}"

    def append(self, event: Event):
        self.events.append(event)
        if str(event.event_id) not in self.counter_events:
            self.counter_events[str(event.event_id)] = {"counter": 1}
        else:
            self.counter_events[str(event.event_id)]["counter"] += 1

    def assert_number_total_events(self, expected_number_events: int):
        actual_number_total_events = len(self.events)
        assert (
            expected_number_events == actual_number_total_events
        ), f"Expected total events is {expected_number_events}, actual {actual_number_total_events}. [{self.counter_events}]"

    def assert_number_unique_events(self, expected_number_events: int):
        actual_number_events = len(self.counter_events.keys())
        assert (
            actual_number_events == expected_number_events
        ), f"Expected events is {expected_number_events}, actual {actual_number_events}. [{self.counter_events}]"

    def get_counter_by_event_id(self, event_id: EventId):
        return self.counter_events.get(str(event_id), {}).get("counter", 0)

    def assert_count_by_event_id(self, event_id: EventId, expected_count: int):
        assert (
            self.get_counter_by_event_id(event_id) == expected_count
        ), f"Expected events is {expected_count}, actual {self.get_counter_by_event_id(event_id)}. [{self.counter_events}]"

    def assert_first_event(self, expected_event: Event):
        self.assert_number_unique_events(1)
        event = self.events[0]
        assert event == expected_event

    def assert_last_event(self, expected_event: Event):
        self.assert_number_unique_events(1)
        event = self.events[-1]
        assert event == expected_event
