import inspect
import time
from os import environ
from typing import Callable, Dict, Any

from dataclasses import dataclass


from petisco.events.publisher.domain.interface_event_publisher import IEventPublisher
from petisco.events.service_deployed import ServiceDeployed
from petisco.events.subscriber.domain.interface_event_subscriber import IEventSubscriber
from petisco.frameworks.interface_application import IApplication
from petisco.logger.interface_logger import INFO, ILogger
from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger
from petisco.notifier.infrastructure.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.notifier.domain.interface_notifier import INotifier
from petisco.notifier.domain.notifier_message import NotifierMessage
from petisco.application.config.config import Config
from petisco.application.singleton import Singleton
from petisco.application.interface_repository import IRepository
from petisco.application.interface_service import IService
from petisco.tasks.infrastructure.apscheduler_task_executor import (
    APSchedulerTaskExecutor,
)
from petisco import __version__


@dataclass
class Petisco(metaclass=Singleton):
    app_name: str
    app_version: str
    logger: ILogger = NotImplementedLogger()
    notifier: INotifier = NotImplementedNotifier()
    application: IApplication = None
    services_provider: Callable = None
    repositories_provider: Callable = None
    options: Dict[str, Any] = None
    info: Dict = None
    _persistence_models: Dict[str, Any] = False
    persistence_configured: bool = False
    config: Config = None
    event_publisher: IEventPublisher = None
    event_subscriber: IEventSubscriber = None
    environment: str = None
    repositories: Dict[str, Any] = None
    services: Dict[str, Any] = None

    def __init__(self, config: Config):
        self.config = config
        self.app_name = config.app_name
        self.app_version = config.app_version
        self.logger = config.get_logger()
        self.environment = environ.get("ENVIRONMENT", None)
        self.info = {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "petisco_version": __version__,
            "environment": self.environment,
            "elapsed_time": {},
        }
        self.notifier = config.get_notifier()
        self._set_persistence()
        self._set_events()
        self.set_tasks()
        self.options = config.options

    @staticmethod
    def get_instance():
        try:
            return Petisco()
        except Exception as e:  # noqa E722
            frame_info = inspect.stack()[1]
            raise ImportError(
                f"Petisco must be configured when the application starts. \n"
                f"Petisco has been requested before its initial configuration.\n "
                f"Following code must be executed after Petisco initialization:\n"
                f"\tfilename: {frame_info.filename}\n"
                f"\tlineno: {frame_info.lineno}\n"
                f"\tfunction: {frame_info.function}\n"
                f"\tcode_context: {frame_info.code_context}"
            )

    @staticmethod
    def from_filename(filename: str):
        """
       Parameters
       ----------
       filename
           YAML-based configuration file (default petisco.yml)
        """
        print(f"Loading petisco from: {filename}")

        config = Config.from_filename(filename).unwrap_or_throw()

        return Petisco(config=config)

    def publish_deploy_event(self):
        if self.config.config_events.publish_deploy_event:
            event = ServiceDeployed(
                app_name=self.app_name, app_version=self.app_version
            )
            self.event_publisher.publish(event)

    def notify_deploy(self):
        self.notifier.publish(
            NotifierMessage(
                title="Service deployed",
                message=f"{self.app_name} has been deployed",
                info_petisco=self.get_info(),
            )
        )

    def set_tasks(self):
        config_tasks = self.config.config_tasks
        if config_tasks.tasks:
            self.info["tasks"] = {}
            for task_name, config_task in config_tasks.tasks.items():
                self.info["tasks"][task_name] = config_task.to_dict()
            self.task_executor = APSchedulerTaskExecutor()

    def _schedule_tasks(self):
        config_tasks = self.config.config_tasks
        if config_tasks.tasks:
            self.task_executor.start(config_tasks)

    def _unschedule_tasks(self):
        self.task_executor.stop()

    def _set_persistence(self):
        self._persistence_models = {}
        config_persistence = self.config.config_persistence
        if config_persistence.config:
            import_database_models_func = (
                config_persistence.get_import_database_models_func()
            )
            config_persistence.config(import_database_models_func)
            self.persistence_configured = True
            self._persistence_models = config_persistence.get_models()

    def _set_services_and_repositories_from_providers(self):
        config_providers = self.config.config_providers
        if not config_providers:
            return
        if config_providers.config_dependencies:
            config_providers.config_dependencies()

        if config_providers.services_provider:

            self.services = self._load_services(config_providers.services_provider)

            info_services = {}
            for key, service in self.services.items():
                if hasattr(service, "info"):
                    info_services[key] = service.info()
                else:
                    raise TypeError(
                        f"Service with key {key} ({type(service)}) must implement info"
                    )
            self.info["services"] = info_services
        if config_providers.repositories_provider:
            self.repositories = self._load_repositories(
                config_providers.repositories_provider
            )
            info_repositories = {}
            for key, repository in self.repositories.items():
                if hasattr(repository, "info"):
                    info_repositories[key] = repository.info()
                else:
                    raise TypeError(
                        f"Repository with key {key} ({type(repository)}) must implement info"
                    )

            self.info["repositories"] = info_repositories

    def _set_events(self):
        config_events = self.config.config_events
        if not config_events:
            return

        if config_events.config_event_publisher.provider:
            self.event_publisher = config_events.config_event_publisher.provider()
            if hasattr(self.event_publisher, "info"):
                self.info["event_publisher"] = self.event_publisher.info()
            else:
                raise TypeError(
                    f"Given event_publisher ({type(self.event_publisher)}) must implement info"
                )

        if config_events.config_event_subscriber.provider:
            subscribers = config_events.config_event_subscriber.subscribers
            self.event_subscriber = config_events.config_event_subscriber.provider(
                subscribers
            )
            if hasattr(self.event_subscriber, "info"):
                self.info["event_subscriber"] = self.event_subscriber.info()
            else:
                raise TypeError(
                    f"Given event_subscriber ({type(self.event_subscriber)}) must implement info"
                )

    def _log_status(self):
        if self.info:
            self.logger.log(INFO, LogMessage(data={"message": {"info": self.info}}))

        if self.options:
            self.logger.log(
                INFO, LogMessage(data={"message": {"options": self.options}})
            )

    def _start(self):
        self.event_subscriber.start()
        self._schedule_tasks()
        self._set_services_and_repositories_from_providers()
        self._log_status()
        self.publish_deploy_event()
        self.notify_deploy()

    def load_services_and_repositories(self):
        self._set_services_and_repositories_from_providers()

    def start(self):
        self._start()
        self.config.get_application().start()

    def get_app(self):
        self._start()
        return self.config.get_application().get_app()

    def stop(self):
        self.event_subscriber.stop()
        self._unschedule_tasks()

    def _load_repositories(self, repositories_provider: Callable):
        start_time = time.time()
        repositories = repositories_provider()
        elapsed_time = time.time() - start_time
        self.info["elapsed_time"][
            "load_repositories"
        ] = f"{int(elapsed_time*1000.0)} ms"
        return repositories

    def _load_services(self, services_provider: Callable):
        start_time = time.time()
        services = services_provider()
        elapsed_time = time.time() - start_time
        self.info["elapsed_time"]["load_services"] = f"{int(elapsed_time*1000.0)} ms"
        return services

    @staticmethod
    def get_service(key: str) -> IService:
        services = Petisco.get_instance().services
        if not services:
            raise ValueError(
                f"Petisco: any service has been declared. Please, add it to petisco.yml."
            )
        service = services.get(key)
        if not service:
            raise ValueError(
                f"Petisco: {key} service is not defined. Please, add it to petisco.yml"
            )
        return service

    @staticmethod
    def get_repository(key: str) -> IRepository:
        repositories = Petisco.get_instance().repositories
        if not repositories:
            raise ValueError(
                f"Petisco: any repository has been declared. Please, add it to petisco.yml"
            )
        repository = repositories.get(key)
        if not repository:
            raise ValueError(
                f"Petisco: {key} repository is not defined. Please, add it to petisco.yml"
            )
        return repository

    @staticmethod
    def persistence_models() -> Dict[str, str]:
        persistence_models = {}
        try:
            persistence_models = Petisco.get_instance()._persistence_models
        except:  # noqa E722
            pass
        return persistence_models

    @staticmethod
    def get_persistence_model(key: str) -> Any:
        return Petisco.persistence_models().get(key)

    @staticmethod
    def persistence_session_scope():
        from petisco.persistence.sqlalchemy.sqlalchemy_session_scope import (
            session_scope,
        )

        return session_scope

    @staticmethod
    def get_event_publisher():
        return Petisco.get_instance().event_publisher

    @staticmethod
    def get_event_subscriber():
        return Petisco.get_instance().event_subscriber

    @staticmethod
    def get_logger():
        return Petisco.get_instance().logger

    @staticmethod
    def get_notifier():
        return Petisco.get_instance().notifier

    @staticmethod
    def get_app_name():
        return Petisco.get_instance().app_name

    @staticmethod
    def get_app_version():
        return Petisco.get_instance().app_version

    @staticmethod
    def get_environment():
        return Petisco.get_instance().environment

    @staticmethod
    def get_info():
        return Petisco.get_instance().info
