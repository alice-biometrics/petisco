import inspect

from typing import Dict, Callable, Any

from dataclasses import dataclass

from petisco.application.repository import Repository
from petisco.application.service import Service
from petisco.application.singleton import Singleton
from petisco.events.interface_event_manager import IEventManager
from petisco.logger.interface_logger import ILogger, INFO, ERROR
from petisco.logger.not_implemented_logger import NotImplementedLogger


@dataclass
class ApplicationConfig(metaclass=Singleton):
    name: str
    mode: str
    logger = ILogger
    services_provider: Callable[[], Dict[str, Service]]
    repositories_provider: Callable[[], Dict[str, Repository]]
    event_manager: IEventManager
    options: Dict[str, Any]
    info: Dict

    @staticmethod
    def get_instance():
        try:
            return ApplicationConfig()
        except:  # noqa E722
            raise ImportError(
                f"ApplicationConfig must be configured when the application starts. ApplicationConfig has been requested before its initial configuration. Incorrectly called by {inspect.stack()[1][3]}"
            )

    def __init__(
        self,
        app_name: str,
        mode: str,
        logger: ILogger = NotImplementedLogger(),
        config_dependencies: Callable = None,
        config_persistence: Callable = None,
        services_mode_mapper: Dict[str, Callable] = None,
        repositories_mode_mapper: Dict[str, Callable] = None,
        event_manager: IEventManager = None,
        options: Dict[str, Any] = None,
    ):
        """
        Parameters
        ----------
        app_name
            Application name
        mode
            DeploymentMode define the toy_app mode of execution. If you're mapping services and repositories, please
            check given mode is mapped in services_mode_mapper and repositories_mode_mapper
        logger
            Pre configured logger
        config_dependencies
            Callable function to configure dependencies (e.g configure credentials in order to connect with a thrid-party
            toy_app.
        config_persistence
            Callable function to configure toy_app persistence (e.g configure a database)
        services_mode_mapper
            A dictionary to map DeploymentMode with a service provider function. This is used as a dependency injector
        repositories_mode_mapper
            A dictionary to map DeploymentMode with a repository provider function. This is used as a dependency injector
        event_manager
            A IEventManager valid implementation
        options
            A dictionary with specific toy_app options
        """

        self.app_name = app_name
        self.mode = mode
        self.logger = logger

        self.logger.log(
            INFO, f"Deploying {self.app_name} application in {self.mode} mode"
        )

        if config_dependencies:
            config_dependencies()

        if config_persistence:
            config_persistence()

        self.info = {}
        if services_mode_mapper:
            if mode not in services_mode_mapper:
                error_message = f"Mode {mode} not found in services_mode_mapper ({services_mode_mapper})"
                self.logger.log(ERROR, error_message)
                raise NotImplementedError(error_message)
            self.services_provider = services_mode_mapper[mode]

            info_services = {}
            for key, service in self.services_provider().items():
                if hasattr(service, "info"):
                    info_services[key] = service.info()
                else:
                    raise TypeError(f"{key} must implement info")
            self.info["services"] = info_services

        if repositories_mode_mapper:
            if mode not in repositories_mode_mapper:
                error_message = f"Mode {mode} not found in repositories_mode_mapper ({repositories_mode_mapper})"
                self.logger.log(ERROR, error_message)
                raise NotImplementedError(error_message)
            self.repositories_provider = repositories_mode_mapper[mode]

            info_repositories = {}
            for key, repository in self.repositories_provider().items():
                if hasattr(repository, "info"):
                    info_repositories[key] = repository.info()
                else:
                    raise TypeError(f"{key} repository must implement info")
            self.info["repositories"] = info_repositories

        if event_manager:
            self.event_manager = event_manager
            if hasattr(event_manager, "info"):
                self.info["event_managers"] = event_manager.info()
            else:
                raise TypeError(f"Given event_manager must implement info")

        self.options = options

        self.logger.log(INFO, f"Info: {self.info}")
        self.logger.log(INFO, f"Options: {self.options}")
