from datetime import datetime

import pytest

from petisco import DomainEvent, Uuid
from petisco.base.domain.message.message import TIME_FORMAT


class MyDomainEvent(DomainEvent):
    name: str


@pytest.mark.unit
def test_domain_event_should_create_domain_event_input_and_output():
    domain_event = MyDomainEvent(name="whatever")

    domain_event_json = domain_event.json()

    retrieved_domain_event = MyDomainEvent.from_json(domain_event_json)

    assert domain_event == retrieved_domain_event
    assert id(domain_event) != id(retrieved_domain_event)


@pytest.mark.unit
def test_domain_event_should_create_domain_event_with_required_values():

    domain_event = MyDomainEvent(name="whatever")

    assert hasattr(domain_event, "attributes")
    assert getattr(domain_event, "attributes") == {"name": "whatever"}
    assert hasattr(domain_event, "message_id")
    assert hasattr(domain_event, "type")
    assert getattr(domain_event, "type") == "domain_event"
    assert hasattr(domain_event, "version")
    assert hasattr(domain_event, "occurred_on")
    assert hasattr(domain_event, "name")
    assert hasattr(domain_event, "attributes")
    assert hasattr(domain_event, "meta")


@pytest.mark.unit
def test_domain_event_should_create_domain_event_input_and_output_with_complex_atributtes():
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
