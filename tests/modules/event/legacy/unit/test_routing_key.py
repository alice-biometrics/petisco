import pytest

from petisco.event.legacy.routing_key import RoutingKey


@pytest.mark.unit
def test_should_create_an_routing_key_and_match_fullname():

    routing_key = RoutingKey("acme.service.1.event.user.created")

    assert routing_key.match_fullname("acme.service.1.event.user.created")


@pytest.mark.unit
@pytest.mark.parametrize(
    "organization,service,version,type_routing_key,expected_result",
    [
        ("acme", "service", 1, "event", True),
        ("acme", None, None, None, True),
        (None, "service", None, None, True),
        (None, None, 1, None, True),
        (None, None, None, "event", True),
        ("invalid", "service", 1, "event", False),
        ("acme", "invalid", 1, "event", False),
        ("invalid", "service", -1, "event", False),
        ("invalid", "service", 1, "invalid", False),
    ],
)
def test_should_create_an_routing_key_and_match(
    organization, service, version, type_routing_key, expected_result
):

    routing_key = RoutingKey("acme.service.1.event.user.created")

    assert (
        routing_key.match(
            organization=organization,
            service=service,
            version=version,
            type_routing_key=type_routing_key,
        )
        == expected_result
    )
