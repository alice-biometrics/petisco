from datetime import datetime
from typing import Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields
from backports.datetime_fromisoformat import MonkeyPatch

from petisco.events.event_id import EventId

MonkeyPatch.patch_fromisoformat()


@dataclass_json
@dataclass
class Event:
    event_id: EventId = None
    event_name: str = None
    occurred_on: datetime = field(
        default=None,
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        ),
    )
    data: Dict[str, Any] = None

    def __init__(self, *args, **kwargs):
        self.occurred_on = kwargs.get("occurred_on", datetime.utcnow())
        self.data = kwargs
        self.event_id = EventId.generate(str(kwargs))
        self.event_name = self.get_event_name()

    @classmethod
    def get_event_name(cls):
        return "{}.{}".format(cls.__module__, cls.__name__)
