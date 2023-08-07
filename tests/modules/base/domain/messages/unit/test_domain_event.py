from datetime import datetime

import pytest

from petisco import DomainEvent, Uuid
from petisco.base.domain.message.message import TIME_FORMAT
from tests.modules.base.domain.messages.unit.domain_events import (
    AttributesDomainEvent,
    MostConflictingDomainEvent,
    MyDomainEvent,
    NameConflictDomainEvent,
    NoAttributesDomainEvent,
    VersionConflictDomainEvent,
)

DOMAIN_EVENTS = [
    NoAttributesDomainEvent(),
    AttributesDomainEvent(id=Uuid.v4().value, username="whatever"),
    NameConflictDomainEvent(name="whatever"),
    VersionConflictDomainEvent(version=100),
]


@pytest.mark.unit
class TestDomainEvent:
    @pytest.mark.parametrize("domain_event", DOMAIN_EVENTS)
    def should_create_domain_event_input_and_output(
        self, domain_event: DomainEvent
    ):  # noqa
        domain_event_json = domain_event.format_json()
        retrieved_domain_event = DomainEvent.from_format(domain_event_json)
        assert domain_event == retrieved_domain_event
        assert id(domain_event) != id(retrieved_domain_event)

    def should_create_domain_event_input_and_output_with_specific_target_type(
        self,
    ):  # noqa
        domain_event = MyDomainEvent(my_specific_value="whatever")

        domain_event_json = domain_event.format_json()

        retrieved_domain_event = MyDomainEvent.from_format(
            domain_event_json, target_type=MyDomainEvent
        )

        assert type(domain_event) is type(domain_event)
        assert domain_event == retrieved_domain_event
        assert id(domain_event) != id(retrieved_domain_event)
        assert (
            domain_event.my_specific_value == retrieved_domain_event.my_specific_value
        )

    def should_create_domain_event_with_required_values(self):  # noqa
        domain_event = MyDomainEvent(my_specific_value="whatever")

        assert hasattr(domain_event, "my_specific_value")
        assert hasattr(domain_event, "_message_attributes")
        assert getattr(domain_event, "_message_attributes") == {
            "my_specific_value": "whatever"
        }
        assert hasattr(domain_event, "_message_id")
        assert hasattr(domain_event, "_message_type")
        assert getattr(domain_event, "_message_type") == "domain_event"
        assert hasattr(domain_event, "_message_version")
        assert hasattr(domain_event, "_message_occurred_on")
        assert hasattr(domain_event, "_message_name")
        assert hasattr(domain_event, "_message_attributes")
        assert hasattr(domain_event, "_message_meta")

    def should_create_domain_event_input_and_output_with_complex_atributtes(
        self,
    ):  # noqa
        class MyDomainEventWithUuid(DomainEvent):
            user_id: Uuid
            created_at: datetime

        user_id = Uuid.from_value("64Eb274A-2906-4670-B479-9751281F5407")
        created_at = datetime.strptime("2021-06-14 18:15:05.329569", TIME_FORMAT)

        domain_event = MyDomainEventWithUuid(user_id=user_id, created_at=created_at)

        domain_event_json = domain_event.format_json()

        retrieved_domain_event = DomainEvent.from_format(domain_event_json)

        assert domain_event == retrieved_domain_event
        assert id(domain_event) != id(retrieved_domain_event)

        assert retrieved_domain_event.get_message_attributes() == {
            "user_id": "64Eb274A-2906-4670-B479-9751281F5407",
            "created_at": "2021-06-14 18:15:05.329569",
        }

    def should_not_share_attributes_between_instances(self):  # noqa
        domain_event1 = MyDomainEvent(
            my_specific_value="whatever",
        )
        domain_event2 = MyDomainEvent(
            my_specific_value="youwant",
        )
        assert (
            domain_event1.get_message_attributes()["my_specific_value"]
            != domain_event2.get_message_attributes()["my_specific_value"]
        )

    def should_create_domain_event_and_keep_message_version_when_exist_a_message_attribute(  # noqa
        self,
    ):
        expected_message_version = 2

        domain_event = VersionConflictDomainEvent(version=100)
        domain_event_json = domain_event.format()
        retrieved_domain_event = DomainEvent.from_format(domain_event_json)

        assert domain_event.get_message_version() == expected_message_version
        assert retrieved_domain_event.get_message_version() == expected_message_version

    def should_create_domain_event_and_keep_message_name_when_exist_a_message_attribute(  # noqa
        self,
    ):
        domain_event = NameConflictDomainEvent(name="whatever")
        domain_event_json = domain_event.format()
        retrieved_domain_event = DomainEvent.from_format(domain_event_json)
        assert domain_event.get_message_name() == "name.conflict.domain.event"
        assert retrieved_domain_event.get_message_name() == "name.conflict.domain.event"

    def should_create_domain_event_with_most_conflicting_domain_event(  # noqa
        self,
    ):
        now = datetime.utcnow()
        domain_event = MostConflictingDomainEvent(
            name="given-name",
            version=2,
            occurred_on=now,
            attributes={"other-attribute": True},
            meta={"client_id": "acme"},
            type="given-type",
        )
        assert domain_event.get_message_name() == "most.conflicting.domain.event"
        assert domain_event.get_message_version() == 2
        assert domain_event.get_message_occurred_on() != now
        assert domain_event.get_message_attributes() == {
            "name": "given-name",
            "version": 2,
            "occurred_on": now,
            "attributes": {"other-attribute": True},
            "meta": {"client_id": "acme"},
            "type": "given-type",
        }
        assert domain_event.get_message_meta() == {}

    def should_create_domain_event_with_correct_name_defined_inside_a_function(  # noqa
        self,
    ):
        class MyInnerDomainEvent(DomainEvent):
            ...

        domain_event = MyInnerDomainEvent()
        assert domain_event.get_message_name() == "my.inner.domain.event"

    def should_retrive_message_type_when_event_is_formated_without_type_message(  # noqa
        self,
    ):
        data = {
            "data": {
                "id": "d679de7a-d9f3-4572-9ced-4b37c459606b",
                "type": "button.pressed",
                "version": "2",
                "occurred_on": "2023-07-13 18:20:02.174000",
                "attributes": {"my_param": "value"},
                "meta": {
                    "platform_name": "Chrome (114.0.0.0)",
                    "system_version": "Mac OS X (Unknown)",
                },
            }
        }

        domain_event = DomainEvent.from_format(data)
        assert domain_event.get_message_type() == "domain_event"
        assert hasattr(domain_event, "my_param")

    def should_be_prepared_to_serialize_a_message_without_attributes(self):
        data_with_null_attributes = '{"data": {"id": "3504bb75-98f9-4073-977c-c2521bebf7c0", "type": "no.attributes.domain.event", "type_message": "domain_event", "version": 1, "occurred_on": "2023-08-07 14:21:47.215225", "attributes": null, "meta": {}}}'
        domain_event = DomainEvent.from_format(data_with_null_attributes)

        assert domain_event.get_message_attributes() == {}

    @pytest.mark.parametrize("domain_event", DOMAIN_EVENTS)
    def should_get_message_info(self, domain_event: DomainEvent):  # noqa
        message_info = type(domain_event).info()
        assert message_info.name == domain_event.get_message_name()
        assert message_info.version == domain_event.get_message_version()
