from __future__ import annotations

import json

import pytest

from petisco import DomainEvent, FileDomainEventBus
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)


@pytest.mark.unit
class TestFileDomainEventBus:
    @pytest.mark.parametrize("domain_event", [DomainEventUserCreatedMother.random()])
    def should_success_on_publish_a_domain_event(
        self, domain_event: DomainEvent | list[DomainEvent], tmp_path
    ):
        filename = tmp_path / "domain_events.json"
        bus = FileDomainEventBus(filename)
        bus.publish(domain_event)

        with open(filename) as file:
            content = file.read()
            domain_events = json.loads(content)
            assert domain_event.get_message_name() == [*domain_events][0]
            assert len(domain_events) == 1

    def should_raise_an_exception_when_input_is_not_valid(self, tmp_path):
        bus = FileDomainEventBus(filename=tmp_path / "domain_events.json")

        with pytest.raises(
            TypeError,
            match="FileDomainEventBus only publishes DomainEvent objects",
        ):
            bus.publish("invalid_input")
