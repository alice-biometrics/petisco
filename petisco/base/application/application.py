from typing import Any, Callable, List, Optional

from pydantic import BaseSettings, Field

from petisco import __version__
from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.dependency_injection.injector import Injector
from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.domain.message.chaos.service_deployed import ServiceDeployed
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.extra.rabbitmq.dependencies import get_default_message_dependencies
from petisco.extra.slack.dependencies import get_default_notifier_dependencies


class Application(BaseSettings):
    name: str
    version: str
    organization: str
    environment: str = Field("local", env="ENVIRONMENT")
    dependencies_provider: Optional[Callable[..., List[Dependency]]] = lambda: []
    configurers: Optional[List[Callable[[bool], Any]]] = []

    def configure(self, testing: bool = False):
        for configurer in self.configurers:
            if configurer:
                try:
                    configurer(testing)
                except TypeError:  # noqa
                    callable_name = getattr(configurer, "__name__", repr(configurer))
                    raise TypeError(
                        f'Given configure function ("{callable_name}") must be defined as Callable[[bool], Any] receiving a boolean as an input.'
                    )
        Injector.set_dependencies(self.get_dependencies())

    def get_dependencies(self) -> List[Dependency]:
        default_dependencies = (
            get_default_message_dependencies() + get_default_notifier_dependencies()
        )
        default_dependencies_dict = {
            dependency.name: dependency for dependency in default_dependencies
        }
        provided_dependencies = self.dependencies_provider()
        given_dependencies_dict = {
            dependency.name: dependency for dependency in provided_dependencies
        }
        merged_dependecies = {**default_dependencies_dict, **given_dependencies_dict}
        return list(merged_dependecies.values())

    def clear(self):
        Injector.clear()

    def info(self):
        info = self.dict()
        info["dependencies"] = {
            dependency.name: dependency.get_instance().info()
            for dependency in self.get_dependencies()
        }
        del info["dependencies_provider"]
        del info["configurers"]
        return info

    def publish_deploy_event(self, domain_event: Optional[DomainEvent] = None):
        try:
            domain_event_bus: DomainEventBus = Injector.get("domain_event_bus")
            domain_event_bus.publish(
                ServiceDeployed(app_name=self.name, app_version=self.version)
            )
        except:  # noqa
            raise TypeError(
                'To publish an event to the domain event bus, please add a dependency with name "domain_event_bus" on Application dependencies'
            )

    def notify_deploy(self):
        try:
            notifier: Notifier = Injector.get("notifier")
            notifier.publish(
                NotifierMessage(
                    title="Service Deployed",
                    message=f"{self.name} (v{self.version}) has been deployed",
                    meta={
                        "app_name": self.name,
                        "app_version": self.version,
                        "petisco_version": __version__,
                        "environment": self.environment,
                    },
                )
            )
        except:  # noqa
            raise TypeError(
                'To notify the deploy, please add a dependency with name "notifier" on Application dependencies'
            )
