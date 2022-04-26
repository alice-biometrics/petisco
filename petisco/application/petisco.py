import inspect
import os
import time
from datetime import datetime
from distutils.util import strtobool
from os import environ
from typing import Callable, Dict, Any

from dataclasses import dataclass
from deprecation import deprecated

from petisco.application.deploy_checker import DeployChecker
from petisco.event.bus.infrastructure.not_implemented_event_bus import (
    NotImplementedEventBus,
)
from petisco.event.configurer.infrastructure.not_implemented_configurer import (
    NotImplementedEventConfigurer,
)
from petisco.event.consumer.infrastructure.not_implemented_event_comsumer import (
    NotImplementedEventConsumer,
)
from petisco.event.legacy.publisher.domain.interface_event_publisher import (
    IEventPublisher,
)
from petisco.event.shared.domain.config_events import ConfigEvents
from petisco.event.shared.domain.service_deployed import ServiceDeployed
from petisco.event.legacy.subscriber.domain.interface_event_subscriber import (
    IEventSubscriber,
)
from petisco.event.shared.domain.service_restarted import ServiceRestarted
from petisco.event.shared.infrastructure.configure_events_infrastructure import (
    configure_events_infrastructure,
)
from petisco.frameworks.interface_application import IApplication
from petisco.logger.interface_logger import INFO, ILogger, ERROR
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
from petisco.application.interface_app_service import IService, IAppService
from petisco.tasks.infrastructure.apscheduler_task_executor import (
    APSchedulerTaskExecutor,
)
from petisco import __version__
from petisco.tasks.infrastructure.not_implemented_task_executor import (
    NotImplementedTaskExecutor,
)


@dataclass
class Petisco(metaclass=Singleton):
    _app_name: str
    _app_version: str
    _logger: ILogger = NotImplementedLogger()
    _notifier: INotifier = NotImplementedNotifier()
    application: IApplication = None
    services_provider: Callable = None
    repositories_provider: Callable = None
    _options: Dict[str, Any] = None
    info: Dict = None
    _persistence_models: Dict[str, Dict[str, Any]] = None
    persistence_sources: Dict[str, Dict] = None
    config: Config = None
    event_publisher: IEventPublisher = None
    event_subscriber: IEventSubscriber = None
    _environment: str = None
    repositories: Dict[str, Any] = None
    services: Dict[str, Any] = None

    def __init__(self, config: Config):
        self.config = config
        self._app_name = config.app_name
        self._app_version = config.app_version
        self._deploy_time = config.deploy_time
        self._logger = config.get_logger()
        self._environment = environ.get("ENVIRONMENT", None)
        self.info = {
            "app_name": self._app_name,
            "app_version": self._app_version,
            "deploy_time": self._deploy_time,
            "petisco_version": __version__,
            "environment": self._environment,
            "elapsed_time": {},
        }
        self._notifier = config.get_notifier()
        self._set_persistence()
        self._set_events_configuration()
        self._set_tasks()
        self._options = config.options
        self._deploy_checker = DeployChecker(
            deploy_time=self._deploy_time,
            courtesy_minutes=int(os.getenv("PETISCO_DEPLOY_COURTESY_MINUTES", 60)),
        )

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
                f"\tcode_context: {frame_info.code_context}\n\n"
                f"\t Possible Solutions:\n"
                f"\t  * If you are testing and need any preconfigured Petisco, you can use the fixture given_any_petisco.\n"
                f"\t  * If you are testing and need specific preconfigured Petisco, you can create a fixture loading a petisco and then clearing.\n"
                f"\t  * If you are running a Petisco application, please review your loading process, petisco.yml is probably failing.\n"
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

    def configure_events(self, filename: str):
        """
        Parameters
        ----------
        filename
            YAML-based event management configuration file (default petisco.events.yml)
        """

        message_broker_type = os.environ.get("PETISCO_EVENT_MESSAGE_BROKER")
        if message_broker_type and message_broker_type == "notimplemented":
            return

        config_events = ConfigEvents.from_filename(filename).unwrap_or_throw()
        (
            self.event_bus,
            self.event_configurer,
            self.event_consumer,
        ) = configure_events_infrastructure(config_events, self._logger)

        if config_events.event_subscribers:
            clear_subscriber_before = strtobool(
                os.getenv(
                    "PETISCO_LEGACY_RABBITMQ_CONFIGURER_CLEAR_SUBSCRIBER_BEFORE",
                    "false",
                )
            )
            clear_store_before = strtobool(
                os.getenv(
                    "PETISCO_LEGACY_RABBITMQ_CONFIGURER_CLEAR_STORE_BEFORE", "false"
                )
            )

            self.event_configurer.configure_subscribers(
                config_events.event_subscribers,
                clear_subscriber_before=clear_subscriber_before,
                clear_store_before=clear_store_before,
            )
            self.event_consumer.add_subscribers(config_events.event_subscribers)
        else:
            self.event_configurer.configure()

        if config_events.store_queue_subscriber:
            self.event_consumer.add_handler_on_store(
                config_events.store_queue_subscriber
            )

        if config_events.queues_subscribers:
            for queue, handlers in config_events.queues_subscribers.items():
                for handler in handlers:
                    self.event_consumer.add_handler_on_queue(queue, handler)

        self.config_events = config_events

        self.info["config_events"] = self.config_events.info()

    def _publish_deploy_event(self):
        if self._deploy_checker.was_recently_deployed(datetime.utcnow()):
            event = ServiceDeployed(
                app_name=self._app_name, app_version=self._app_version
            )
        else:
            event = ServiceRestarted(
                app_name=self._app_name, app_version=self._app_version
            )

        if self.config_events and self.config_events.publish_deploy_event:
            self.event_bus.publish(event)

        # Legacy Approach
        if self.config.config_events.publish_deploy_event:
            self.event_publisher.publish(event)

    def _notify_restart(self):
        if not self._deploy_checker.was_recently_deployed(datetime.utcnow()):
            self._notifier.publish(
                NotifierMessage(
                    title="Service Restarted",
                    message=f"{self._app_name} has been restarted. Original deploy was at {self._deploy_checker.get_deploy_time()}",
                    info_petisco=self.get_info(),
                )
            )

    def _set_tasks(self):
        config_tasks = self.config.config_tasks
        if config_tasks and config_tasks.tasks:
            self.info["tasks"] = {}
            for task_name, config_task in config_tasks.tasks.items():
                self.info["tasks"][task_name] = config_task.to_dict()
            self.task_executor = APSchedulerTaskExecutor()
        else:
            self.task_executor = NotImplementedTaskExecutor()

    def _schedule_tasks(self):
        config_tasks = self.config.config_tasks
        if config_tasks.tasks:
            self.task_executor.start(config_tasks)

    def _unschedule_tasks(self):
        config_tasks = self.config.config_tasks
        if config_tasks.tasks:
            self.task_executor.stop()

    def _set_persistence(self):
        self._persistence_models = {}
        self.persistence_sources = {}
        config_persistence = self.config.config_persistence
        if config_persistence and config_persistence.configs:
            for config_key, config_value in config_persistence.configs.items():
                if config_value.type == "sql":
                    import_database_models_func = (
                        config_persistence.get_import_database_models_func(config_key)
                    )

                    config_value.config(import_database_models_func)

                    self._persistence_models[
                        config_key
                    ] = config_persistence.get_models(config_key)
                else:
                    config_value.config()
                self.persistence_sources[config_key] = {
                    "configured": True,
                    "type": config_value.type,
                }

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

    def _set_events_configuration(self):
        self.event_bus = NotImplementedEventBus()
        self.event_configurer = NotImplementedEventConfigurer()
        self.event_consumer = NotImplementedEventConsumer()
        self.config_events = None

        self._legacy_set_events_configuration()

    def _legacy_set_events_configuration(self):
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
            self._logger.log(INFO, LogMessage(data={"message": {"info": self.info}}))

        if self._options:
            self._logger.log(
                INFO, LogMessage(data={"message": {"options": self._options}})
            )

    def _start(self):
        self._set_services_and_repositories_from_providers()
        self.event_subscriber.start()
        self.event_consumer.start()
        self._schedule_tasks()
        self._log_status()
        self._announce()

    def _announce(self):
        try:
            self._publish_deploy_event()
            self._notify_restart()
        except Exception as exc:
            log_message = LogMessage(layer="petisco")
            log_message.set_message(
                f"Error announcing alice-petisco application {str(exc)}"
            )
            self._logger.log(ERROR, log_message)

    def load_services_and_repositories(self):
        self._set_services_and_repositories_from_providers()

    def start(self):
        self._start()
        self._application.start()

    def get_app(self):
        self._start()
        self._application = self.config.get_application()
        return self._application.get_app()

    def get_application(self):
        return self._application

    def stop(self):
        self.event_subscriber.stop()
        self.event_consumer.stop()
        self._unschedule_tasks()

    def _load_repositories(self, repositories_provider: Callable):
        start_time = time.time()
        repositories = repositories_provider()
        elapsed_time = time.time() - start_time
        self.info["elapsed_time"][
            "load_repositories"
        ] = f"{int(elapsed_time * 1000.0)} ms"
        return repositories

    def _load_services(self, services_provider: Callable):
        start_time = time.time()
        services = services_provider()
        elapsed_time = time.time() - start_time
        self.info["elapsed_time"]["load_services"] = f"{int(elapsed_time * 1000.0)} ms"
        return services

    @staticmethod
    def get_event_bus():
        return Petisco.get_instance().event_bus

    @staticmethod
    def get_event_consumer():
        return Petisco.get_instance().event_consumer

    @staticmethod
    def get_logger():
        return Petisco.get_instance()._logger

    @staticmethod
    def get_notifier():
        return Petisco.get_instance()._notifier

    @staticmethod
    def get_app_name():
        return Petisco.get_instance()._app_name

    @staticmethod
    def get_app_version():
        return Petisco.get_instance()._app_version

    @staticmethod
    def get_environment():
        return Petisco.get_instance()._environment

    @staticmethod
    def get_info():
        return Petisco.get_instance().info

    # TODO Remove deprecated options
    @staticmethod
    @deprecated("This method is deprecated. Please, use AppServices.get()")
    def get_app_service(key: str) -> IAppService:
        services = Petisco.get_instance().services
        if not services:
            raise ValueError(
                "Petisco: no service has been declared. Please, add it to petisco.yml."
            )
        service = services.get(key)
        if not service:
            raise ValueError(
                f"Petisco: {key} service is not defined. Please, add it to petisco.yml"
            )
        return service

    @staticmethod
    @deprecated("This method is deprecated. Please, use AppServices.get()")
    def get_service(key: str) -> IService:
        return Petisco.get_app_service(key)

    @staticmethod
    @deprecated("This method is deprecated. Please, use Repositories.get()")
    def get_repository(key: str) -> IRepository:
        repositories = Petisco.get_instance().repositories
        if repositories is None:
            raise ValueError(
                "Petisco: no repository has been declared. Please, add it to petisco.yml"
            )
        repository = repositories.get(key)
        if not repository:
            raise ValueError(
                f"Petisco: {key} repository is not defined. Please, add it to petisco.yml"
            )
        return repository

    @staticmethod
    def persistence_models(persistence_entry: str) -> Dict[str, str]:
        persistence_models = {}
        try:
            persistence_models = Petisco.get_instance()._persistence_models[
                persistence_entry
            ]
        except:  # noqa E722
            pass
        return persistence_models

    @staticmethod
    def get_persistence_model(persistence_entry: str, key: str) -> Any:
        return Petisco.persistence_models(persistence_entry).get(key)

    @staticmethod
    def persistence_mongodb_client():
        from petisco.persistence.pymongo.pymongo_persistence import PyMongoPersistence

        return PyMongoPersistence().client

    @staticmethod
    @deprecated("This method is deprecated.")
    def get_event_publisher():
        return Petisco.get_instance().event_publisher

    @staticmethod
    @deprecated("This method is deprecated.")
    def get_event_subscriber():
        return Petisco.get_instance().event_subscriber
