import uuid
import validators

from petisco.domain.value_objects.value_object import ValueObjectError, ValueObject


class InvalidUuidError(ValueObjectError):
    def __init__(self, uuid_value: str):
        self.message = f"{self.__class__.__name__}: [uuid: {uuid_value}]"


class Uuid(ValueObject):
    @staticmethod
    def length():
        return 36

    def __init__(self, value: str, execute_guard: bool = True):
        self.value = value
        super(Uuid, self).__init__(execute_guard)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.value}]"

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.value == other.value
        else:
            return False

    def guard(self):
        self._ensure_is_valid_uuid(self.value)

    def _ensure_is_valid_uuid(self, value):
        if value is None or not validators.uuid(value):
            raise InvalidUuidError(value)

    @classmethod
    def generate(cls):
        return cls(str(uuid.uuid4()))
