import pytest

from petisco import DomainEvent


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
    assert getattr(domain_event, "type") == "application"
    assert hasattr(domain_event, "version")
    assert hasattr(domain_event, "occurred_on")
    assert hasattr(domain_event, "name")
    assert hasattr(domain_event, "attributes")
    assert hasattr(domain_event, "meta")
