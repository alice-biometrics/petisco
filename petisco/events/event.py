from datetime import datetime
from typing import Dict

from petisco.events.event_id import EventId

import json


class Event:
    event_id: EventId = None
    event_name: str = None
    event_occurred_on: str = None
    event_version: str = None
    event_info_id: Dict = None

    def __init__(self, dictionary=None):
        if dictionary:
            self.__dict__.update(dictionary)

        self.event_id = (
            EventId.generate(str(dictionary)) if not self.event_id else self.event_id
        )
        self.event_name = (
            self.__class__.__name__ if not self.event_name else self.event_name
        )
        self.event_occurred_on = (
            datetime.utcnow() if not self.event_occurred_on else self.event_occurred_on
        )

    def __repr__(self):
        return f"[{self.event_name}: {json.loads(self.to_json())}]"

    def __eq__(self, other):
        if (
            isinstance(other, self.__class__)
            or issubclass(other.__class__, self.__class__)
            or issubclass(self.__class__, other.__class__)
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self) -> Dict:
        return self.__dict__

    @staticmethod
    def from_dict(dictionary: Dict):
        if "event_id" in dictionary and isinstance(dictionary["event_id"], str):
            dictionary["event_id"] = EventId(dictionary["event_id"])
        if "event_occurred_on" in dictionary and isinstance(
            dictionary["event_occurred_on"], str
        ):
            dictionary["event_occurred_on"] = datetime.strptime(
                dictionary["event_occurred_on"], "%Y-%m-%d %H:%M:%S.%f"
            )
        return Event(dictionary)

    def to_json(self):
        return json.dumps(self.to_dict(), default=self._datetime_to_str)

    def _datetime_to_str(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    @staticmethod
    def from_json(event_json):
        event_dict = json.loads(event_json)
        return Event.from_dict(event_dict)

    def add_info_id(self, info_id):
        from petisco.domain.aggregate_roots.info_id import (
            InfoId,
        )  # internal import to avoid circular dependency

        if not isinstance(info_id, InfoId):
            raise TypeError("Event.add_info_id() expect a InfoId class (from petisco)")
        self.event_info_id = info_id.to_dict()
        return self
