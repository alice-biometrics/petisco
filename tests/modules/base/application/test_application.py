import functools
from datetime import datetime
from typing import List, NoReturn

import pytest

from petisco import (
    Application,
    ApplicationConfigurer,
    Container,
    Dependency,
    DomainEvent,
    NotifierMessage,
)
from tests.modules.base.mothers.dependency_mother import DependencyMother


def testing_with_empty_container(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        Container.clear()
        result = func(*args, **kwargs)
        Container.clear()
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
@testing_with_empty_container
def test_application_should_construct_from_required_variables():

    deployed_at = datetime(year=2021, month=10, day=25, hour=11, minute=11)

    application = Application(
        name="service", version="1.0.0", organization="acme", deployed_at=deployed_at
    )
    application.configure()

    assert DEFAULT_AVAILABLE_DEPENDENCIES == Container.get_available_dependencies()
    assert {
        "name": "service",
        "version": "1.0.0",
        "organization": "acme",
        "deployed_at": deployed_at.strftime("%m/%d/%Y, %H:%M:%S"),
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
@testing_with_empty_container
def test_application_should_construct_and_configure_with_testing_variable():

    Application(name="service", version="1.0.0", organization="acme").configure(
        testing=True
    )

    assert DEFAULT_AVAILABLE_DEPENDENCIES == Container.get_available_dependencies()


@pytest.mark.unit
@testing_with_empty_container
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
        == Container.get_available_dependencies()
    )


@pytest.mark.unit
@testing_with_empty_container
def test_application_should_construct_with_a_dependency_overwrite():
    def dependencies_provider() -> List[Dependency]:
        return [DependencyMother.domain_event_bus()]

    Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies_provider=dependencies_provider,
    ).configure()

    assert DEFAULT_AVAILABLE_DEPENDENCIES == Container.get_available_dependencies()


@pytest.mark.unit
@testing_with_empty_container
def test_application_should_construct_with_configurers():
    class MyApplicationConfigurer(ApplicationConfigurer):
        def execute(self, testing: bool = False) -> NoReturn:
            pass

    Application(
        name="service",
        version="1.0.0",
        organization="acme",
        configurers=[
            MyApplicationConfigurer(),
            MyApplicationConfigurer(execute_after_dependencies=True),
        ],
    ).configure()


@pytest.mark.unit
@testing_with_empty_container
def test_application_should_raise_an_exception_when_configurer_with_an_exeption():
    class MyApplicationConfigurer(ApplicationConfigurer):
        def execute(self, testing: bool = False) -> NoReturn:
            raise RuntimeError("Our Error")

    with pytest.raises(RuntimeError) as excinfo:
        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            configurers=[MyApplicationConfigurer()],
        ).configure()
    assert "Our Error" in str(excinfo.value)


@pytest.mark.unit
@testing_with_empty_container
def test_application_should_publish_a_domain_event():
    def dependencies_provider() -> List[Dependency]:
        return [DependencyMother.domain_event_bus()]

    application = Application(
        name="service",
        version="1.0.0",
        organization="acme",
        dependencies_provider=dependencies_provider,
    )
    application.configure()

    class MyDomainEvent(DomainEvent):
        pass

    application.publish_domain_event(MyDomainEvent())


@pytest.mark.unit
@testing_with_empty_container
def test_application_should_notify_a_message():
    deployed_at = datetime(year=2021, month=10, day=25, hour=11, minute=11)

    application = Application(
        name="service", version="1.0.0", organization="acme", deployed_at=deployed_at
    )
    application.configure()

    message = NotifierMessage(
        title=f":thinking_face: {application.name} is restarted",
        meta={
            "application": f"{application.name} (v{application.version.rstrip()})",
            "environment": application.environment,
            "deployed_at": application.deployed_at.strftime("%m/%d/%Y, %H:%M:%S"),
        },
    )
    application.notify(message)
