import inspect
from typing import Callable, Dict, Any

from dataclasses import dataclass
from dotmap import DotMap

from petisco.events.interface_event_manager import IEventManager
from petisco.events.service_deployed import ServiceDeployed
from petisco.frameworks.interface_application import IApplication
from petisco.logger.interface_logger import INFO, ILogger
from petisco.application.config.config import Config
from petisco.application.singleton import Singleton
from petisco.logger.not_implemented_logger import NotImplementedLogger

DEPLOY_TOPIC = "deploy"


@dataclass
class Petisco(metaclass=Singleton):
    app_name: str
    app_version: str
    logger: ILogger = NotImplementedLogger()
    application: IApplication = None
    services_provider: Callable = None
    repositories_provider: Callable = None
    event_manager_provider: Callable = None
    options: Dict[str, Any] = None
    info: Dict = None
    _persistence_models: Dict[str, Any] = False
    persistence_configured: bool = False
    config: Config = None
    event_topic: str = None

    def __init__(self, config: Config):
        self.config = config
        self.app_name = config.app_name
        self.app_version = config.app_version
        self.logger = config.get_logger()
        self.info = {}
        self.set_persistence(config)
        self.set_infrastructure(config)
        self.options = config.options

        if self.info:
            self.logger.log(INFO, f"Info: {self.info}")

        if self.options:
            self.logger.log(INFO, f"Options: {self.options}")

        if self.config.config_infrastructure.publish_deploy_event_func:
            event_manager = self.config.config_infrastructure.event_manager_provider()
            event = ServiceDeployed(
                app_name=self.app_name, app_version=self.app_version
            )
            event_manager.publish(topic=DEPLOY_TOPIC, event=event)

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

    def set_persistence(self, config):
        config_persistence = config.config_persistence
        import_database_models_func = (
            config_persistence.get_import_database_models_func()
        )
        if config_persistence.config:
            config_persistence.config(import_database_models_func)
            self.persistence_configured = True

        self._persistence_models = config_persistence.get_models()

    def set_infrastructure(self, config):
        config_infrastructure = config.config_infrastructure
        if not config_infrastructure:
            return
        if config_infrastructure.config_dependencies:
            config_infrastructure.config_dependencies()

        if config_infrastructure.services_provider:
            self.services_provider = config_infrastructure.services_provider

            info_services = {}
            for key, service in self.services_provider().items():
                if hasattr(service, "info"):
                    info_services[key] = service.info()
                else:
                    raise TypeError(
                        f"Service with key {key} ({type(service)}) must implement info"
                    )
            self.info["services"] = info_services
        if config_infrastructure.repositories_provider:
            self.repositories_provider = config_infrastructure.repositories_provider

            info_repositories = {}
            for key, repository in self.repositories_provider().items():
                if hasattr(repository, "info"):
                    info_repositories[key] = repository.info()
                else:
                    raise TypeError(
                        f"Repository with key {key} ({type(repository)}) must implement info"
                    )

            self.info["repositories"] = info_repositories
        if config_infrastructure.event_manager_provider:
            self.event_manager_provider = config_infrastructure.event_manager_provider
            event_manager = self.event_manager_provider()
            if hasattr(event_manager, "info"):
                self.info["event_managers"] = event_manager.info()
            else:
                raise TypeError(
                    f"Given event_manager ({type(event_manager)}) must implement info"
                )

        if config_infrastructure.event_topic:
            self.event_topic = config_infrastructure.event_topic

    def start(self):
        self.config.get_application().start()

    def get_app(self):
        return self.config.get_application().get_app()

    @staticmethod
    def services() -> DotMap:
        return DotMap(Petisco.get_instance().services_provider())

    @staticmethod
    def repositories() -> DotMap:
        return DotMap(Petisco.get_instance().repositories_provider())

    @staticmethod
    def persistence_models() -> DotMap:
        persistence_models = {}
        try:
            persistence_models = Petisco.get_instance()._persistence_models
        except:  # noqa E722
            pass
        return persistence_models

    @staticmethod
    def persistence_session_scope():
        from petisco.persistence.sqlalchemy.sqlalchemy_session_scope import (
            session_scope,
        )

        return session_scope

    @staticmethod
    def event_manager() -> IEventManager:
        return Petisco.get_instance().event_manager_provider()

    @staticmethod
    def providers():
        return Petisco.services(), Petisco.repositories(), Petisco.event_manager()
