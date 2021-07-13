from typing import Callable, List, Optional

from pydantic import BaseSettings, Field

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.dependency_injection.injector import Injector
from petisco.base.domain.message.chaos.service_deployed import ServiceDeployed
from petisco.base.domain.message.domain_event import DomainEvent


class Application(BaseSettings):
    name: str = Field(..., env="APPLICATION_NAME")
    version: str = Field(..., env="APPLICATION_VERSION")
    organization: str = Field(..., env="ORGANIZATION")
    testing: bool = Field(..., env="TEST")
    dependencies: Optional[List[Dependency]]
    configurers: Optional[List[Callable]]

    class Config:
        env_prefix = "PETISCO_"

    def start(self):
        Injector.set_dependencies(self.dependencies)

        for configurer in self.configurers:
            if configurer:
                configurer(self.testing)

    def publish_deploy_event(self, domain_event: Optional[DomainEvent]):
        domain_event_bus = Injector.get("domain_event_bus")

        if not domain_event:
            domain_event = ServiceDeployed(app_name=self.name, app_version=self.version)

        domain_event_bus.publish(domain_event)
