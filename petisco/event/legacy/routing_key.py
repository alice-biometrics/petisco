from typing import Any

from meiga import Result, Error, Success

from petisco.domain.value_objects.value_object import ValueObject


class RoutingKey(ValueObject):
    def __init__(self, value: str):
        self.value = None if value == "None" else value
        if self.value:
            try:
                (
                    self.organization,
                    self.service,
                    self.version,
                    self.type_routing_key,
                ) = self.value.split(".")[:4]
                self.event_name = ".".join(self.value.split(".")[4:])
                self.version = int(self.version)
            except ValueError:
                pass

    def __repr__(self):
        return f"[RoutingKey: {self.value}"

    def to_result(self) -> Result[Any, Error]:
        value = None if self == "None" else self
        return Success(value)

    def match_fullname(self, fullname):
        is_equal = False
        if fullname == self.value:
            is_equal = True
        return is_equal

    def match(
        self,
        organization: str = None,
        service: str = None,
        version: int = None,
        type_routing_key: str = None,
    ):
        is_equal = True
        if organization and organization != self.organization:
            is_equal = False
        if service and service != self.service:
            is_equal = False
        if version and version != self.version:
            is_equal = False
        if type_routing_key and type_routing_key != self.type_routing_key:
            is_equal = False
        return is_equal
