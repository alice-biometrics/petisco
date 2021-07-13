from typing import Any, Callable, List, Optional

from pydantic import BaseSettings, Field

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.dependency_injection.injector import Injector
from petisco.base.domain.message.chaos.service_deployed import ServiceDeployed
from petisco.base.domain.message.domain_event import DomainEvent


class Application(BaseSettings):
    name: str = Field(..., env="APPLICATION_NAME")
    version: str = Field(..., env="APPLICATION_VERSION")
    organization: str = Field(..., env="ORGANIZATION")
    testing: bool = Field(False, env="TEST")
    dependencies: Optional[List[Dependency]] = []
    configurers: Optional[List[Callable[[bool], Any]]] = []

    class Config:
        env_prefix = "PETISCO_"

    def configure(self):

        # default_dependencies = []

        dependencies = self.dependencies

        Injector.set_dependencies(dependencies)

        for configurer in self.configurers:
            if configurer:
                try:
                    configurer(self.testing)
                except:  # noqa
                    callable_name = getattr(configurer, "__name__", repr(configurer))
                    raise TypeError(
                        f'Given configure function ("{callable_name}") must be defined as Callable[[bool], Any] receiving a boolean as an input.'
                    )

    def clear(self):
        Injector.clear()

    def publish_deploy_event(self, domain_event: Optional[DomainEvent] = None):
        try:
            domain_event_bus = Injector.get("domain_event_bus")
            if not domain_event:
                domain_event = ServiceDeployed(
                    app_name=self.name, app_version=self.version
                )
            domain_event_bus.publish(domain_event)
        except:  # noqa
            raise TypeError(
                'To publish an event to the domain event bus, please add a dependency with "domain_event_bus" on Application dependencies'
            )
