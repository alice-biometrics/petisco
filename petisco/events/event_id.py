from petisco.domain.value_objects.uuid import Uuid
from petisco.domain.value_objects.value_object import ValueObjectError


class InvalidEventIdError(ValueObjectError):
    def __init__(self, uuid_value: str):
        self.message = f"{self.__class__.__name__}: [uuid: {uuid_value}]"


class EventId(Uuid):

    # overwritten to maintain compatibility with legacy events
    def guard(self):
        self._ensure_is_36_char_uuid()

    def _ensure_is_36_char_uuid(self):
        if len(self.value) != 36:
            raise InvalidEventIdError(self.value)
