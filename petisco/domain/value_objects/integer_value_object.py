from petisco.domain.value_objects.value_object import ValueObject


class IntegerValueObject(ValueObject):
    def __init__(self, value: int):
        super(IntegerValueObject, self).__init__()
        self.value = value

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

    def to_str(self):
        return str(self.value)
