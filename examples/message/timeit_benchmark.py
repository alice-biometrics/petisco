from __future__ import annotations

from timeit import default_number, timeit

model_dump = True
format_dump = False


def run_test(domain_event) -> None:
    if model_dump:
        dumped = domain_event.model_dump()
        _ = domain_event.__class__(**dumped)

    if format_dump:
        formatted = domain_event.format()
        _ = domain_event.__class__.from_format(formatted)


def use_message_inheriting_from_pydantic() -> None:
    from petisco import DomainEvent, Uuid

    class MyDomainEvent(DomainEvent):
        name: str
        age: int
        id: Uuid

    domain_event = MyDomainEvent(name="MrBean", age=65, id=Uuid.v4())

    run_test(domain_event, model_dump, format)


def use_legacy_message() -> None:
    from petisco import Uuid
    from petisco.base.domain.message.legacy.legacy_domain_event import LegacyDomainEvent

    class MyDomainEvent(LegacyDomainEvent):
        name: str
        age: int
        id: Uuid

    domain_event = MyDomainEvent(name="MrBean", age=65, id=Uuid.v4())

    run_test(domain_event)


time_success = timeit(lambda: use_message_inheriting_from_pydantic())
print(f"time with pydantic: {(time_success/default_number)*1000000000} ns")

time_success = timeit(lambda: use_legacy_message())
print(f"time with legacy: {(time_success/default_number)*1000000000} ns")
