from datetime import datetime
from typing import Dict

from petisco.controller.correlation_id import CorrelationId
from petisco.events.event_id import EventId

import json


class Event:
    id: EventId = None
    name: str = None
    occurred_on: str = None
    version: str = None
    correlation_id: CorrelationId = None

    def __init__(self, dictionary=None):
        if dictionary:
            self.__dict__.update(dictionary)

        self.id = EventId.generate(str(dictionary)) if not self.id else self.id
        self.name = self.__class__.__name__ if not self.name else self.name
        self.occurred_on = (
            datetime.utcnow() if not self.occurred_on else self.occurred_on
        )

    def __repr__(self):
        return f"[{self.name}: {json.loads(self.to_json())}]"

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
        if "id" in dictionary and isinstance(dictionary["id"], str):
            dictionary["id"] = EventId(dictionary["id"])
        if "occurred_on" in dictionary and isinstance(dictionary["occurred_on"], str):
            dictionary["occurred_on"] = datetime.strptime(
                dictionary["occurred_on"], "%Y-%m-%d %H:%M:%S.%f"
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
