import functools

import pytest

from petisco import Application, Injector
from tests.modules.base.mothers.dependency_mother import DependencyMother


def testing_with_empty_injector(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        Injector.clear()
        result = func(*args, **kwargs)
        Injector.clear()
        return result

    return wrapper


DEFAULT_AVAILABLE_DEPENDENCIES = [
    "domain_event_bus",
    "command_bus",
    "domain_event_consumer",
    "command_consumer",
    "notifier",
]


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_from_required_variables():

    application = Application(name="service", version="1.0.0", organization="acme")

    application.configure()

    assert DEFAULT_AVAILABLE_DEPENDENCIES == Injector.get_available_dependencies()
    assert {
        "name": "service",
        "version": "1.0.0",
        "organization": "acme",
        "environment": "local",
        "testing": False,
        "dependencies": {
            "domain_event_bus": {"name": "NotImplementedDomainEventBus"},
            "command_bus": {"name": "NotImplementedDomainEventBus"},
            "domain_event_consumer": {"name": "NotImplementedMessageConsumer"},
            "command_consumer": {"name": "NotImplementedMessageConsumer"},
            "notifier": {"name": "NotImplementedNotifier"},
        },
    } == application.info()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_with_testing_variable():

    application = Application(
        name="service", version="1.0.0", organization="acme", testing=True
    )

    application.configure()
    assert DEFAULT_AVAILABLE_DEPENDENCIES == Injector.get_available_dependencies()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_with_dependencies():

    application = Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies=[DependencyMother.any()],
    )

    application.configure()

    assert (
        DEFAULT_AVAILABLE_DEPENDENCIES + ["repo"]
        == Injector.get_available_dependencies()
    )


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_with_a_dependency_overwrite():

    application = Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies=[DependencyMother.domain_event_bus()],
    )

    application.configure()

    assert DEFAULT_AVAILABLE_DEPENDENCIES == Injector.get_available_dependencies()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_with_configurers():
    def configurer(testing: bool):
        pass

    application = Application(
        name="service",
        version="1.0.0",
        organization="acme",
        configurers=[configurer, configurer],
    )

    application.configure()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_raise_an_exception_when_configurer_do_not_receive_a_boolean_value():
    def configurer():
        pass

    with pytest.raises(TypeError) as excinfo:
        application = Application(
            name="service",
            version="1.0.0",
            organization="acme",
            configurers=[configurer],
        )
        application.configure()

    assert (
        'Given configure function ("configurer") must be defined as Callable[[bool], Any] receiving a boolean as an input.'
        in str(excinfo.value)
    )


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_publish_service_deployed_domain_event():

    application = Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies=[DependencyMother.domain_event_bus()],
    )
    application.configure()
    application.publish_deploy_event()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_notify_deploy():

    application = Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies=[DependencyMother.domain_event_bus()],
    )
    application.configure()
    application.notify_deploy()


# @pytest.mark.unit
# @testing_with_empty_injector
# def test_application_should_raise_an_exception_when_publish_deploy_event_and_none_dependency_domain_event_bus_is_defined():
#
#     with pytest.raises(TypeError) as excinfo:
#         application = Application(
#             name="service",
#             version="1.0.0",
#             organization="acme",
#             dependencies=[]
#         )
#         application.configure()
#
#         application.publish_deploy_event()
#     assert "To publish an event to the domain event bus, please add a dependency with \"domain_event_bus\" on Application dependencies" in str(excinfo.value)
#


# @pytest.mark.unit
# def test_application_should_construct_from_required_variables():
#
#     _ = Application(
#         name="service",
#         version="1.0.0",
#         organization="acme",
#         testing=True
#     )

# name: str = Field(..., env="APPLICATION_NAME")
# version: str = Field(..., env="APPLICATION_VERSION")
# organization: str = Field(..., env="ORGANIZATION")
# testing: bool = Field(False, env="TEST")
# dependencies: Optional[List[Dependency]]
# configurers: Optional[List[Callable]]
