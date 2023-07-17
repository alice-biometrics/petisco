from __future__ import annotations

import pyperf

model_dump = False
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

    run_test(domain_event)


def use_legacy_message() -> None:
    from petisco import Uuid
    from petisco.base.domain.message.legacy.legacy_domain_event import LegacyDomainEvent

    class MyDomainEvent(LegacyDomainEvent):
        name: str
        age: int
        id: Uuid

    domain_event = MyDomainEvent(name="MrBean", age=65, id=Uuid.v4())

    run_test(domain_event)


runner = pyperf.Runner()
runner.bench_func("construction (pydantic)", use_message_inheriting_from_pydantic)
runner.bench_func("construction (legacy)", use_legacy_message)
