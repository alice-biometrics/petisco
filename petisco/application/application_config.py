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
    services_provider: Callable[[], Dict[str, Service]]
    repositories_provider: Callable[[], Dict[str, Repository]]
    event_manager: IEventManager
    options: Dict[str, Any]
    info: Dict

    @staticmethod
    def get_instance():
        return ApplicationConfig()

    def __init__(
        self,
        mode: str,
        logger: ILogger = NotImplementedLogger(),
        config_dependencies: Callable = None,
        config_persistence: Callable = None,
        services_mode_mapper: Dict[str, Callable] = None,
        repositories_mode_mapper: Dict[str, Callable] = None,
        event_manager_mapper: Dict[str, Callable] = None,
        options: Dict[str, Any] = None,
    ):
        """

        Parameters
        ----------
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
        event_manager_mapper
            A dictionary to map DeploymentMode with a event manager provider function. This is used as a dependency injector
        options
            A dictionary with specific toy_app options
        """

        self.mode = mode
        self.logger = logger
        if self.logger:
            self.logger.log(INFO, "Deploying in {} mode".format(mode))

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

        if event_manager_mapper:
            if mode not in event_manager_mapper:
                error_message = f"Mode {mode} not found in event_manager_mapper ({event_manager_mapper})"
                self.logger.log(ERROR, error_message)
                raise NotImplementedError(error_message)
            self.event_manager_provider = event_manager_mapper[mode]

            info_event_managers = {}
            for key, event_manager in self.event_manager_provider().items():
                if hasattr(event_manager, "info"):
                    info_event_managers[key] = event_manager.info()
                else:
                    raise TypeError(f"{key} event_manager must implement info")
            self.info["event_managers"] = info_event_managers

        self.options = options

        if self.logger:
            self.logger.log(INFO, f"Info: {self.info}")
            self.logger.log(INFO, f"Options: {self.options}")
