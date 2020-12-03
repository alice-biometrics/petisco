import base64
import os

from petisco.domain.value_objects.uuid import Uuid
from petisco.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
)

LENGTH = 16


class UserId(Uuid):
    @classmethod
    def generate_legacy(cls):
        r = os.urandom(LENGTH)
        return cls(
            base64.b64encode(r, altchars=b"-_").decode("utf-8")[:LENGTH],
            execute_guard=False,
        )

    @classmethod
    def from_legacy(cls, legacy_value: str):
        if len(legacy_value) > LENGTH:
            raise ExceedLengthLimitValueObjectError(message=legacy_value)
        return cls(legacy_value, execute_guard=False)
