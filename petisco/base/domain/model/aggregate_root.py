from abc import ABC
from copy import copy
from inspect import isclass
from typing import Any, Dict, List, Union, get_args

from pydantic import (
    BaseModel,
    Field,
    NonNegativeInt,
    PrivateAttr,
    field_serializer,
    field_validator,
    model_validator,
)

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.model.value_object import ValueObject

DEFAULT_VERSION = 1


class AggregateRoot(ABC, BaseModel):
    """
    A base class to define AggregateRoot

    It is a cluster of associated entities that are treated as a unit for the purpose of data changes.
    """

    aggregate_id: Uuid = Field(default_factory=Uuid.v4)
    aggregate_version: NonNegativeInt = Field(default=DEFAULT_VERSION)
    _domain_events: List[DomainEvent] = PrivateAttr(default=[])

    @model_validator(mode="before")
    def model_validation(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        new_data = copy(data)
        for key, annotation in cls.__annotations__.items():
            value = data.get(key)
            if value is None:
                continue

            union_annotations = get_args(annotation)
            if len(union_annotations) > 0:
                for union_annotation in union_annotations:
                    if (
                        isclass(union_annotation)
                        and issubclass(union_annotation, ValueObject)
                        and isinstance(value, str)
                    ):
                        new_value = union_annotation(value=value)
                        new_data[key] = new_value
            else:
                if isclass(annotation) and issubclass(annotation, ValueObject) and isinstance(value, str):
                    new_value = annotation(value=value)
                    new_data[key] = new_value
        return new_data

    @field_serializer("aggregate_id")
    def serialize_aggregate_id(self, aggregate_id: Uuid) -> str:
        return aggregate_id.value

    @field_validator("aggregate_id", mode="before")
    def set_aggregate_id(cls, v: Union[str, Uuid]) -> Uuid:
        v = Uuid(value=v) if isinstance(v, str) else v
        return v or Uuid.v4()

    @field_validator("aggregate_version", mode="before")
    def set_aggregate_version(cls, v: NonNegativeInt) -> NonNegativeInt:
        return v or DEFAULT_VERSION

    def record(self, domain_event: DomainEvent) -> None:
        """
        Record something that happened is our domain related with the aggregate (a DomainEvent).
        """
        self._domain_events.append(domain_event)

    def clear_domain_events(self) -> None:
        """
        Clear all domain events recorded.
        """
        self._domain_events = []

    def pull_domain_events(self) -> List[DomainEvent]:
        """
        Returns and clear all domain events recorded.
        """
        domain_events = copy(self._domain_events)
        self.clear_domain_events()
        return domain_events

    def get_domain_events(self) -> List[DomainEvent]:
        """
        Returns all domain events recorded.
        """
        return self._domain_events

    def get_first_domain_event(self) -> Union[DomainEvent, None]:
        """
        Returns only the first domain event recorded.
        """
        return self._domain_events[0] if len(self._domain_events) > 0 else None

    def get_last_domain_event(self) -> Union[DomainEvent, None]:
        """
        Returns only the last domain event recorded.
        """
        return self._domain_events[-1] if len(self._domain_events) > 0 else None
