from datetime import datetime

import pytest

from petisco import DomainEvent, Uuid
from petisco.base.domain.message.message import TIME_FORMAT


class MyDomainEvent(DomainEvent):
    my_specific_value: str


@pytest.mark.unit
class TestDomainEvent:
    def should_create_domain_event_input_and_output(self):
        domain_event = MyDomainEvent(my_specific_value="whatever")

        domain_event_json = domain_event.json()

        retrieved_domain_event = MyDomainEvent.from_json(domain_event_json)

        assert domain_event == retrieved_domain_event
        assert id(domain_event) != id(retrieved_domain_event)

    def should_create_domain_event_input_and_output_with_specigic_target_type(self):
        domain_event = MyDomainEvent(my_specific_value="whatever")

        domain_event_json = domain_event.json()

        retrieved_domain_event = MyDomainEvent.from_json(
            domain_event_json, target_type=MyDomainEvent
        )

        assert type(domain_event) == type(domain_event)
        assert domain_event == retrieved_domain_event
        assert id(domain_event) != id(retrieved_domain_event)
        assert (
            domain_event.my_specific_value == retrieved_domain_event.my_specific_value
        )

    def should_create_domain_event_with_required_values(self):

        domain_event = MyDomainEvent(my_specific_value="whatever")

        assert hasattr(domain_event, "my_specific_value")
        assert hasattr(domain_event, "attributes")
        assert getattr(domain_event, "attributes") == {"my_specific_value": "whatever"}
        assert hasattr(domain_event, "message_id")
        assert hasattr(domain_event, "type")
        assert getattr(domain_event, "type") == "domain_event"
        assert hasattr(domain_event, "version")
        assert hasattr(domain_event, "occurred_on")
        assert hasattr(domain_event, "name")
        assert hasattr(domain_event, "attributes")
        assert hasattr(domain_event, "meta")

    def should_create_domain_event_input_and_output_with_complex_atributtes(self):
        class MyDomainEventWithUuid(DomainEvent):
            user_id: Uuid
            created_at: datetime

        user_id = Uuid.from_value("64Eb274A-2906-4670-B479-9751281F5407")
        created_at = datetime.strptime("2021-06-14 18:15:05.329569", TIME_FORMAT)

        domain_event = MyDomainEventWithUuid(user_id=user_id, created_at=created_at)

        domain_event_json = domain_event.json()

        retrieved_domain_event = MyDomainEvent.from_json(domain_event_json)

        assert domain_event == retrieved_domain_event
        assert id(domain_event) != id(retrieved_domain_event)

        assert retrieved_domain_event.attributes == {
            "user_id": "64Eb274A-2906-4670-B479-9751281F5407",
            "created_at": "2021-06-14 18:15:05.329569",
        }

    def should_not_share_attributes_between_instances(self):
        domain_event1 = MyDomainEvent(
            my_specific_value="whatever", foo="hola", bar="mundo"
        )
        domain_event2 = MyDomainEvent(
            my_specific_value="youwant", foo="hola2", bar="mundo2"
        )
        assert domain_event1.attributes["foo"] != domain_event2.attributes["foo"]
        assert domain_event1.attributes["bar"] != domain_event2.attributes["bar"]
