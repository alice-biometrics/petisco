import functools
from typing import List

import pytest

from petisco import Application, Dependency, Injector
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
    "message_configurer",
    "message_consumer",
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
        "dependencies": {
            "domain_event_bus": {"name": "NotImplementedDomainEventBus"},
            "command_bus": {"name": "NotImplementedCommandBus"},
            "message_configurer": {"name": "NotImplementedMessageConfigurer"},
            "message_consumer": {"name": "NotImplementedMessageConsumer"},
            "notifier": {"name": "NotImplementedNotifier"},
        },
    } == application.info()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_and_configure_with_testing_variable():

    Application(name="service", version="1.0.0", organization="acme").configure(
        testing=True
    )

    assert DEFAULT_AVAILABLE_DEPENDENCIES == Injector.get_available_dependencies()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_with_dependencies_provider():
    def dependencies_provider() -> List[Dependency]:
        return [DependencyMother.any()]

    Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies_provider=dependencies_provider,
    ).configure()

    assert (
        DEFAULT_AVAILABLE_DEPENDENCIES + ["repo"]
        == Injector.get_available_dependencies()
    )


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_with_a_dependency_overwrite():
    def dependencies_provider() -> List[Dependency]:
        return [DependencyMother.domain_event_bus()]

    Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies_provider=dependencies_provider,
    ).configure()

    assert DEFAULT_AVAILABLE_DEPENDENCIES == Injector.get_available_dependencies()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_construct_with_configurers():
    def configurer(testing: bool):
        pass

    Application(
        name="service",
        version="1.0.0",
        organization="acme",
        configurers=[configurer, configurer],
    ).configure()


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_raise_an_exception_when_configurer_do_not_receive_a_boolean_value():
    def configurer():
        pass

    with pytest.raises(TypeError) as excinfo:
        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            configurers=[configurer],
        ).configure()
    assert (
        'Given configure function ("configurer") must be defined as Callable[[bool], Any] receiving a boolean as an input.'
        in str(excinfo.value)
    )


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_raise_an_exception_when_configurer_with_an_exeption():
    def configurer(testing: bool):
        raise RuntimeError("Our Error")

    with pytest.raises(RuntimeError) as excinfo:
        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            configurers=[configurer],
        ).configure()
    assert "Our Error" in str(excinfo.value)


@pytest.mark.unit
@testing_with_empty_injector
def test_application_should_publish_service_deployed_domain_event():
    def dependencies_provider() -> List[Dependency]:
        return [DependencyMother.domain_event_bus()]

    application = Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies_provider=dependencies_provider,
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
    )
    application.configure()
    application.notify_deploy()
