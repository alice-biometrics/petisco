import base64
import os

from petisco.domain.value_objects.uuid import Uuid
from petisco.domain.errors.exceed_length_limit_value_error_error import (
    ExceedLengthLimitValueObjectError,
)

LENGTH = 16


class UserId(Uuid):
    def guard(self):
        self._ensure_is_16_char_uuid()

    def _ensure_is_16_char_uuid(self):
        if len(self.value) > LENGTH:
            raise ExceedLengthLimitValueObjectError(message=self.value)

    @classmethod
    def generate(cls):
        # TODO: refactor to cls(str(uuid.uuid4()))
        r = os.urandom(LENGTH)
        return cls(base64.b64encode(r, altchars=b"-_").decode("utf-8")[:LENGTH])
