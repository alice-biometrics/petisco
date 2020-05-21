import re
from datetime import datetime
from typing import Dict

from petisco.events.event_id import EventId, EVENT_ID_LENGTH

import json

from typing import List

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Event:
    event_id: EventId = None
    event_name: str = None
    event_occurred_on: str = None
    event_version: int = None
    event_info_id: Dict = None

    def __init__(self, dictionary=None):

        self.event_version = 1

        if dictionary:
            self.__dict__.update(dictionary)
            self.event_version = dictionary.get("event_version", 1)

        self._set_id()
        self._set_name()
        self._set_occurred_on()

    def _set_id(self):
        self.event_id = EventId.generate() if not self.event_id else self.event_id

    def _set_name(self):
        self.event_name = (
            self.__class__.__name__ if not self.event_name else self.event_name
        )
        self.event_name = (
            re.sub(r"(?<!^)(?=[A-Z])", "_", self.event_name).lower().replace("_", ".")
        )

    def _set_occurred_on(self):
        self.event_occurred_on = (
            datetime.utcnow() if not self.event_occurred_on else self.event_occurred_on
        )

    def __repr__(self):
        return f"{json.loads(self.to_json())}"

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

        raw_dict = self.__dict__.copy()
        data = {
            "data": {
                "id": str(raw_dict.pop("event_id")),
                "type": raw_dict.pop("event_name"),
                "version": str(raw_dict.pop("event_version")),
                "occurred_on": raw_dict.pop("event_occurred_on").strftime(TIME_FORMAT),
                "attributes": {},
                "meta": {},
            }
        }

        if "event_info_id" in raw_dict:
            if raw_dict.get("event_info_id"):
                data["data"]["meta"]["info_id"] = raw_dict.get("event_info_id")
            raw_dict.pop("event_info_id")

        data["data"]["attributes"] = raw_dict

        return data

    @staticmethod
    def from_dict(jsonapi: Dict):

        data = jsonapi.get("data")

        event_dictionary = {}

        if "id" in data and isinstance(data["id"], str):
            event_dictionary["event_id"] = EventId(data["id"])

        if "type" in data and isinstance(data["type"], str):
            event_dictionary["event_name"] = EventId(data["type"])

        if "version" in data and isinstance(data["version"], str):
            event_dictionary["event_version"] = int(data["version"])

        if "occurred_on" in data and isinstance(data["occurred_on"], str):
            event_dictionary["event_occurred_on"] = datetime.strptime(
                data["occurred_on"], TIME_FORMAT
            )

        event_dictionary["event_info_id"] = data.get("meta", {}).get("info_id")

        event_dictionary.update(data.get("attributes"))

        return Event(event_dictionary)

    @staticmethod
    def from_deprecated_dict(deprecated_dict: Dict):
        if "event_id" in deprecated_dict and isinstance(
            deprecated_dict["event_id"], str
        ):
            new_event_id = deprecated_dict["event_id"].rjust(EVENT_ID_LENGTH, "0")
            deprecated_dict["event_id"] = EventId(new_event_id)
        if "event_occurred_on" in deprecated_dict and isinstance(
            deprecated_dict["event_occurred_on"], str
        ):
            deprecated_dict["event_occurred_on"] = datetime.strptime(
                deprecated_dict["event_occurred_on"], TIME_FORMAT
            )

        if (
            "event_version" in deprecated_dict
            and isinstance(deprecated_dict["event_version"], str)
            and len(deprecated_dict["event_version"]) > 1
        ):
            deprecated_dict["event_version"] = "0"

        info_id = None
        if "info_id" in deprecated_dict and isinstance(
            deprecated_dict["info_id"], dict
        ):
            from petisco.domain.aggregate_roots.info_id import InfoId

            info_id = InfoId.from_dict(deprecated_dict.pop("info_id"))

        event = Event(deprecated_dict)
        event.add_info_id(info_id)

        return event

    def to_json(self):
        return json.dumps(self.to_dict(), default=self._datetime_to_str)

    def _datetime_to_str(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    @staticmethod
    def from_json(event_json):
        event_dict = json.loads(event_json)
        return Event.from_dict(event_dict)

    @staticmethod
    def from_deprecated_json(event_json):
        event_dict = json.loads(event_json)
        return Event.from_deprecated_dict(event_dict)

    def add_info_id(self, info_id):
        if not info_id:
            return self

        from petisco.domain.aggregate_roots.info_id import (
            InfoId,
        )  # internal import to avoid circular dependency

        if not isinstance(info_id, InfoId):
            raise TypeError("Event.add_info_id() expect a InfoId class (from petisco)")
        self.event_info_id = info_id.to_dict()
        return self


Events = List[Event]
