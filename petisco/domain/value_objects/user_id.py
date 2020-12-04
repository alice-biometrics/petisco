import base64
import os
import re

from petisco.domain.value_objects.uuid import Uuid, InvalidUuidError

LENGTH = 16


class UserId(Uuid):
    @classmethod
    def generate_legacy(cls):
        return cls(LegacyUserId.generate().value, execute_guard=False)

    def __init__(self, value, execute_guard: bool = True):
        try:
            super(UserId, self).__init__(value, execute_guard=execute_guard)
        except InvalidUuidError:
            legacy_user_id = LegacyUserId(value)
            super(UserId, self).__init__(legacy_user_id.value, execute_guard=False)


class LegacyUserId(Uuid):
    def guard(self):
        self._ensure_is_16_char_uuid()
        self._ensure_value_contains_valid_char()

    def _ensure_is_16_char_uuid(self):
        if self.value is None or len(self.value) != LENGTH:
            raise InvalidUuidError(self.value)

    def _ensure_value_contains_valid_char(self, allow_utf8mb4: bool = True):
        if not isinstance(self.value, str) or not re.search(
            r"^[\w]*(([',. -][\s]?[\w]?)?[\w]*)*$", self.value
        ):
            raise InvalidUuidError(self.value)
        if not allow_utf8mb4 and re.match("[^\u0000-\uffff]", self.value):
            raise InvalidUuidError(self.value)

    @classmethod
    def generate(cls):
        # TODO: refactor to cls(str(uuid.uuid4()))
        r = os.urandom(LENGTH)
        return cls(base64.b64encode(r, altchars=b"-_").decode("utf-8")[:LENGTH])
