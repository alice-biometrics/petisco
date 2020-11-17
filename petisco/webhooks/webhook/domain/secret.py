from meiga import Error

from petisco.domain.value_objects.string_value_object import StringValueObject


class SecretIsNotHexError(Error):
    def __init__(self, message):
        self.message = message


class Secret(StringValueObject):
    def guard(self):
        try:
            int(self.value, 16)
        except ValueError:
            raise SecretIsNotHexError(self.value)
        pass

    def get_bytes(self) -> bytes:
        return bytes(self.value, "utf-8")
