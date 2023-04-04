from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List

from loguru import logger
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
    deployed_at: datetime
    environment: str = Field("local", env="ENVIRONMENT")
    dependencies_provider: Callable[..., List[Dependency]] = lambda: []
    configurers: List[ApplicationConfigurer] = []

    def __init__(self, **data: Any) -> None:
        info = ApplicationInfo(
            name=data["name"],
            organization=data["organization"],
            version=data["version"],
            deployed_at=data.get("deployed_at"),
            force_recreation=True,
        )
        deployed_at = info.deployed_at.strftime("%m/%d/%Y, %H:%M:%S")
        logger.info(
            f"Application: {info.name} {info.version} ({info.organization}) deployed at {deployed_at}"
        )
        super().__init__(**data)

    def configure(
        self, testing: bool = False, overwrite_dependencies: bool = False
    ) -> None:

        before_dependencies_configurers = [
            configurer
            for configurer in self.configurers
            if configurer.execute_after_dependencies is False
        ]
        name_configurers = [
            configurer.__class__.__name__
            for configurer in before_dependencies_configurers
        ]
        logger.info(
            f"Application: running configurators before setting dependencies {name_configurers}..."
        )
        for configurer in before_dependencies_configurers:
            configurer.execute(testing)

        logger.info("Application: setting dependencies...")
        Container.set_dependencies(self.get_dependencies(), overwrite_dependencies)

        after_dependencies_configurers = [
            configurer
            for configurer in self.configurers
            if configurer.execute_after_dependencies is True
        ]

        name_configurers = [
            configurer.__class__.__name__
            for configurer in after_dependencies_configurers
        ]
        logger.info(
            f"Application: running configurators after setting dependencies {name_configurers}..."
        )
        for configurer in after_dependencies_configurers:
            configurer.execute(testing)

        logger.info("Application: successful configuration")

    def get_dependencies(self) -> List[Dependency]:
        # TODO: review default dependencies in v2

        default_dependencies = (
            get_default_message_dependencies() + get_default_notifier_dependencies()
        )
        # TODO: the `dependency.type if not dependency.name else dependency.name` will be deprecated in v2 -> use
        #  just `dependency.type` as key
        default_dependencies_dict = {
            dependency.get_key(): dependency for dependency in default_dependencies
        }
        provided_dependencies = self.dependencies_provider()
        provided_dependencies_dict = {
            dependency.get_key(): dependency for dependency in provided_dependencies
        }
        # This merged_dependencies will give preference to provided_dependencies_dict over default_dependencies_dict
        merged_dependencies = {
            **default_dependencies_dict,
            **provided_dependencies_dict,
        }
        return list(merged_dependencies.values())

    def clear(self) -> None:
        Container.clear()

    def info(self) -> Dict[str, Any]:
        info = self.dict()
        info["deployed_at"] = self.deployed_at.strftime("%m/%d/%Y, %H:%M:%S")

        info["dependencies"] = {
            dependency.type.__name__: dependency.get_instance().info()
            for dependency in self.get_dependencies()
        }
        del info["dependencies_provider"]
        del info["configurers"]
        return info

    def was_deploy_few_minutes_ago(self, minutes: int = 25) -> bool:
        return datetime.utcnow() < self.deployed_at + timedelta(minutes=minutes)

    def publish_domain_event(self, domain_event: DomainEvent) -> None:
        try:
            domain_event_bus = Container.get(DomainEventBus)
            domain_event_bus.publish(domain_event)
        except Exception as exc:  # noqa
            raise TypeError(
                f"To publish an event to the domain event bus, please add a dependency with type `DomainEventBus` on Application dependencies. {str(exc)}"
            )

    def notify(self, message: NotifierMessage) -> None:
        try:
            notifier = Container.get(Notifier)
            notifier.publish(message)
        except:  # noqa
            raise TypeError(
                'To notify the deploy, please add a dependency with name "notifier" on Application dependencies'
            )
