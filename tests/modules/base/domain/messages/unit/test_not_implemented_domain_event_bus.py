from __future__ import annotations

import pytest

from petisco import DomainEvent, NotImplementedDomainEventBus
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)


@pytest.mark.unit
class TestNotImplementedDomainEventBus:
    @pytest.mark.parametrize("domain_event", [DomainEventUserCreatedMother.random()])
    def should_success_on_publish_a_domain_event(self, domain_event: DomainEvent | list[DomainEvent]):
        bus = NotImplementedDomainEventBus()
        bus.publish(domain_event)

    def should_raise_an_exception_when_input_is_not_valid(self):
        bus = NotImplementedDomainEventBus()

        with pytest.raises(
            TypeError,
            match="NotImplementedDomainEventBus only publishes DomainEvent objects",
        ):
            bus.publish("invalid_input")
