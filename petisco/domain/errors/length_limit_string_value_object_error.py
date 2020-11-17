from petisco.domain.value_objects.value_object import ValueObjectError


class ExceedLengthLimitValueObjectError(ValueObjectError):
    def __init__(self, message):
        self.message = message


class NotReachMinimumValueObjectError(ValueObjectError):
    def __init__(self, message):
        self.message = message


class NotHasSpecificLengthValueObjectError(ValueObjectError):
    def __init__(self, message):
        self.message = message
