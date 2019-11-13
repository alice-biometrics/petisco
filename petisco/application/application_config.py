from typing import Dict, Callable, Any

from dataclasses import dataclass

from petisco.application.repository import Repository
from petisco.application.service import Service
from petisco.application.singleton import Singleton
from petisco.events.event_manager import EventManager
from petisco.logger.logger import Logger, INFO, ERROR


@dataclass
class ApplicationConfig(metaclass=Singleton):
    services_provider: Callable[[], Dict[str, Service]]
    repositories_provider: Callable[[], Dict[str, Repository]]
    event_manager: EventManager
    options: Dict[str, Any]
    info: Dict

    @staticmethod
    def get_instance():
        return ApplicationConfig()

    def __init__(
        self,
        mode: str,
        logger: Logger,
        config_dependencies: Callable = None,
        config_persistence: Callable = None,
        services_mode_mapper: Dict[str, Callable] = None,
        repositories_mode_mapper: Dict[str, Callable] = None,
        event_manager: EventManager = None,
        options: Dict[str, Any] = None,
    ):
        """

        Parameters
        ----------
        mode
            DeploymentMode define the application mode of execution. If you're mapping services and repositories, please
            check given mode is mapped in services_mode_mapper and repositories_mode_mapper
        logger
            Pre configured logger
        config_dependencies
            Callable function to configure dependencies (e.g configure credentials in order to connect with a thrid-party
            application.
        config_persistence
            Callable function to configure application persistence (e.g configure a database)
        services_mode_mapper
            A dictionary to map DeploymentMode with a service provider function. This is used as a dependency injector
        repositories_mode_mapper
            A dictionary to map DeploymentMode with a repository provider function. This is used as a dependency injector
        event_manager
            Pre configured event manager. For intance, a event manager that uses Redis for messaging
        options
            A dictionary with specific application options
        """

        self.mode = mode
        self.logger = logger
        self.logger.log(INFO, "Deploying in {} mode".format(mode))

        if config_dependencies:
            config_dependencies()

        if config_persistence:
            config_persistence()

        self.info = {}
        if services_mode_mapper:
            if mode not in services_mode_mapper:
                self.logger.log(
                    ERROR,
                    f"Mode {mode} not found in services_mode_mapper ({services_mode_mapper})",
                )
                raise NotImplementedError(
                    f"Mode {mode} not found in services_mode_mapper ({services_mode_mapper})"
                )
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
                self.logger.log(
                    ERROR,
                    f"Mode {mode} not found in repositories_mode_mapper ({repositories_mode_mapper})",
                )
                raise NotImplementedError(
                    f"Mode {mode} not found in repositories_mode_mapper ({repositories_mode_mapper})"
                )
            self.repositories_provider = repositories_mode_mapper[mode]

            info_repositories = {}
            for key, repository in self.repositories_provider().items():
                if hasattr(repository, "info"):
                    info_repositories[key] = repository.info()
                else:
                    raise TypeError(f"{key} repository must implement info")
            self.info["repositories"] = info_repositories

        self.event_manager = event_manager
        self.options = options

        self.logger.log(INFO, f"Info: {self.info}")
        self.logger.log(INFO, f"{self.event_manager}")
        self.logger.log(INFO, f"Options: {self.options}")
