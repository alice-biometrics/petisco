from datetime import datetime, timedelta
from typing import Callable, List, Optional

from pydantic import BaseSettings, Field

from petisco.base.application.application_configurer import ApplicationConfigurer
from petisco.base.application.application_info import ApplicationInfo
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.extra.rabbitmq.dependencies import get_default_message_dependencies
from petisco.extra.slack.dependencies import get_default_notifier_dependencies


class Application(BaseSettings):
    name: str
    version: str
    organization: str
    deployed_at: Optional[datetime]
    environment: str = Field("local", env="ENVIRONMENT")
    dependencies_provider: Optional[Callable[..., List[Dependency]]] = lambda: []
    configurers: Optional[List[ApplicationConfigurer]] = []

    def __init__(self, **data) -> None:
        ApplicationInfo(
            name=data["name"],
            organization=data["organization"],
            version=data["version"],
            deployed_at=data.get("deployed_at"),
        )
        super().__init__(**data)

    def configure(self, testing: bool = False):

        before_dependecies_configurers = [
            configurer
            for configurer in self.configurers
            if configurer.execute_after_dependencies is False
        ]
        for configurer in before_dependecies_configurers:
            configurer.execute(testing)

        Container.set_dependencies(self.get_dependencies())

        after_dependencies_configurers = [
            configurer
            for configurer in self.configurers
            if configurer.execute_after_dependencies is True
        ]
        for configurer in after_dependencies_configurers:
            configurer.execute(testing)

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
        Container.clear()

    def info(self):
        info = self.dict()
        info["deployed_at"] = (
            self.deployed_at.strftime("%m/%d/%Y, %H:%M:%S")
            if self.deployed_at
            else None
        )
        info["dependencies"] = {
            dependency.name: dependency.get_instance().info()
            for dependency in self.get_dependencies()
        }
        del info["dependencies_provider"]
        del info["configurers"]
        return info

    def was_deploy_few_minutes_ago(self, minutes: int = 25):
        return datetime.utcnow() < self.deployed_at + timedelta(minutes=minutes)

    def publish_domain_event(self, domain_event: DomainEvent):
        try:
            domain_event_bus: DomainEventBus = Container.get("domain_event_bus")
            domain_event_bus.publish(domain_event)
        except:  # noqa
            raise TypeError(
                'To publish an event to the domain event bus, please add a dependency with name "domain_event_bus" on Application dependencies'
            )

    def notify(self, message: NotifierMessage):
        try:
            notifier: Notifier = Container.get("notifier")
            notifier.publish(message)
        except:  # noqa
            raise TypeError(
                'To notify the deploy, please add a dependency with name "notifier" on Application dependencies'
            )
