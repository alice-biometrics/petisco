from __future__ import annotations

import functools
from datetime import datetime
from typing import Any, NoReturn

import pytest

from petisco import (
    Application,
    ApplicationConfigurer,
    Builder,
    Container,
    Dependency,
    DomainError,
    DomainEvent,
    DomainEventBus,
    HttpError,
    NotifierMessage,
    NotImplementedDomainEventBus,
)
from petisco.base.application.application_info import ApplicationInfo
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    BaseRepo,
    MyOtherRepo,
    MyRepo,
    OtherBaseRepo,
)
from tests.modules.base.mothers.dependency_mother import DependencyMother


def testing_with_empty_container(func):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        Container.clear()
        result = func(*args, **kwargs)
        Container.clear()
        return result

    return wrapper


DEFAULT_AVAILABLE_DEPENDENCIES = [
    "DomainEventBus",
    "CommandBus",
    "MessageConfigurer",
    "MessageConsumer",
    "Notifier",
]


@pytest.mark.unit
class TestApplication:
    @testing_with_empty_container
    def should_construct_from_required_variables(self):

        deployed_at = datetime(year=2021, month=10, day=25, hour=11, minute=11)

        application = Application(
            name="service",
            version="1.0.0",
            organization="acme",
            deployed_at=deployed_at,
        )
        application.configure()
        assert DEFAULT_AVAILABLE_DEPENDENCIES == Container.get_available_dependencies()
        expected_info = {
            "name": "service",
            "version": "1.0.0",
            "organization": "acme",
            "deployed_at": deployed_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "environment": "local",
            "dependencies": {
                "DomainEventBus": {"name": "NotImplementedDomainEventBus"},
                "CommandBus": {"name": "NotImplementedCommandBus"},
                "MessageConfigurer": {"name": "NotImplementedMessageConfigurer"},
                "MessageConsumer": {"name": "NotImplementedMessageConsumer"},
                "Notifier": {"name": "NotImplementedNotifier"},
            },
        }
        assert expected_info == application.info()

    @testing_with_empty_container
    def should_construct_and_configure_with_testing_variable(self):

        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            deployed_at=datetime.utcnow(),
        ).configure(testing=True)

        assert DEFAULT_AVAILABLE_DEPENDENCIES == Container.get_available_dependencies()

    @testing_with_empty_container
    def should_construct_and_instantiate_application_info_singleton(self):

        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            deployed_at=datetime.utcnow(),
        )

        assert ApplicationInfo().name == "service"
        assert ApplicationInfo().version == "1.0.0"
        assert ApplicationInfo().organization == "acme"

        ApplicationInfo.clear()

    @testing_with_empty_container
    def should_construct_with_dependencies_provider(self):
        def dependencies_provider() -> list[Dependency]:
            return [DependencyMother.any()]

        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            dependencies_provider=dependencies_provider,
            deployed_at=datetime.utcnow(),
        ).configure()

        assert (
            DEFAULT_AVAILABLE_DEPENDENCIES + ["BaseRepo"]
            == Container.get_available_dependencies()
        )

    @testing_with_empty_container
    @pytest.mark.skip  # We have to define how this is going to work on v2 (default or not default dependencies)
    def should_raise_an_exception_when_construct_with_a_existent_dependency(self):
        def dependencies_provider() -> list[Dependency]:
            return [DependencyMother.domain_event_bus()]

        with pytest.raises(IndexError, match="Container: dependency"):
            Application(
                name="service",
                version="1.0.0",
                organization="acme",
                dependencies_provider=dependencies_provider,
                deployed_at=datetime.utcnow(),
            ).configure()

    @testing_with_empty_container
    def should_construct_with_a_dependency_overwrite(self):
        def dependencies_provider() -> list[Dependency]:
            return [DependencyMother.domain_event_bus()]

        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            dependencies_provider=dependencies_provider,
            deployed_at=datetime.utcnow(),
        ).configure(overwrite_dependencies=True)

        assert DEFAULT_AVAILABLE_DEPENDENCIES == Container.get_available_dependencies()

    @testing_with_empty_container
    def should_construct_adding_an_existent_dependency_with_an_alias(self):
        def dependencies_provider() -> list[Dependency]:
            return [
                Dependency(
                    DomainEventBus,
                    alias="other-domain-event-bus",
                    builders={"default": Builder(NotImplementedDomainEventBus)},
                )
            ]

        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            dependencies_provider=dependencies_provider,
            deployed_at=datetime.utcnow(),
        ).configure()

        assert (
            DEFAULT_AVAILABLE_DEPENDENCIES + ["other-domain-event-bus"]
            == Container.get_available_dependencies()
        )

    @testing_with_empty_container
    def should_construct_with_configurers(self):
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
            deployed_at=datetime.utcnow(),
        ).configure()

    @testing_with_empty_container
    def should_raise_an_exception_when_a_configurer_raise_an_exception(self):
        class MyApplicationConfigurer(ApplicationConfigurer):
            def execute(self, testing: bool = False) -> NoReturn:
                raise RuntimeError("Our Error")

        with pytest.raises(RuntimeError) as excinfo:
            Application(
                name="service",
                version="1.0.0",
                organization="acme",
                configurers=[MyApplicationConfigurer()],
                deployed_at=datetime.utcnow(),
            ).configure()
        assert "Our Error" in str(excinfo.value)

    @testing_with_empty_container
    def should_publish_a_domain_event(self):
        def dependencies_provider() -> list[Dependency]:
            return [DependencyMother.domain_event_bus()]

        application = Application(
            name="service",
            version="1.0.0",
            organization="acme",
            dependencies_provider=dependencies_provider,
            deployed_at=datetime.utcnow(),
        )
        application.configure(overwrite_dependencies=True)

        class MyDomainEvent(DomainEvent):
            pass

        application.publish_domain_event(MyDomainEvent())

    @testing_with_empty_container
    def should_notify_a_message(self):
        deployed_at = datetime(year=2021, month=10, day=25, hour=11, minute=11)

        application = Application(
            name="service",
            version="1.0.0",
            organization="acme",
            deployed_at=deployed_at,
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

    @testing_with_empty_container
    def should_construct_and_configure_with_two_provided_dependencies(self):

        deployed_at = datetime(year=2021, month=10, day=25, hour=11, minute=11)

        def dependencies_provider() -> list[Dependency]:
            return [
                Dependency(BaseRepo, builders={"default": Builder(MyRepo)}),
                Dependency(OtherBaseRepo, builders={"default": Builder(MyOtherRepo)}),
            ]

        application = Application(
            name="service",
            version="1.0.0",
            organization="acme",
            deployed_at=deployed_at,
            dependencies_provider=dependencies_provider,
        )
        application.configure()

        assert (
            DEFAULT_AVAILABLE_DEPENDENCIES + ["BaseRepo", "OtherBaseRepo"]
            == Container.get_available_dependencies()
        )
        assert issubclass(type(Container.get(BaseRepo)), BaseRepo)
        assert issubclass(type(Container.get(OtherBaseRepo)), OtherBaseRepo)

    @testing_with_empty_container
    def should_construct_with_shared_error_map(self):
        class MyNotFoundError(DomainError):
            ...

        shared_error_map = {MyNotFoundError: HttpError(status_code=404)}

        Application(
            name="service",
            version="1.0.0",
            organization="acme",
            deployed_at=datetime(year=2021, month=10, day=25, hour=11, minute=11),
            shared_error_map=shared_error_map,
        )

        application_info = ApplicationInfo()

        assert shared_error_map == application_info.shared_error_map
