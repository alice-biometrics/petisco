import secrets

from meiga import Error

from petisco.domain.value_objects.string_value_object import StringValueObject


class SecretIsNotHexError(Error):
    def __init__(self, message):
        self.message = message


class Secret(StringValueObject):
    @staticmethod
    def generate():
        return Secret(secrets.token_hex(20))

    def guard(self):
        self._ensure_hex()
        self._ensure_value_has_specific_length(40)

    def _ensure_hex(self):
        try:
            int(self.value, 16)
        except ValueError:
            raise SecretIsNotHexError(self.value)

    def get_bytes(self) -> bytes:
        return bytes(self.value, "utf-8")
