import inspect

from petisco.logger.interface_logger import INFO
from petisco.application.config.config import Config
from petisco.application.singleton import Singleton


class Petisco(metaclass=Singleton):
    @staticmethod
    def get_instance():
        try:
            return Petisco()
        except:  # noqa E722
            raise ImportError(
                f"Petisco must be configured when the application starts. Petisco has been requested before its initial configuration. Incorrectly called by {inspect.stack()[1][3]}"
            )

    def __init__(self, filename: str):
        """
       Parameters
       ----------
       filename
           YAML-based configuration file (default petisco.yml)
        """
        print(filename)
        config = Config.from_filename(filename).unwrap_or_throw()

        self.app_name = config.app_name
        self.app_version = config.app_version
        self.logger = config.get_logger()
        self.application = config.get_application()
        self.persistence_configured = False
        self.info = {}
        self.services_provider = None
        self.repositories_provider = None
        self.event_manager_provider = None
        self.set_infrastructure(config)
        self.options = config.options

        if self.info:
            self.logger.log(INFO, f"Info: {self.info}")

        if self.options:
            self.logger.log(INFO, f"Options: {self.options}")

    def set_infrastructure(self, config):
        config_infrastructure = config.config_infrastructure
        if config_infrastructure.config_dependencies:
            config_infrastructure.config_dependencies()
        if config_infrastructure.config_persistence:
            config_infrastructure.config_persistence()
            self.persistence_configured = True
        if config_infrastructure.services_provider:
            self.services_provider = config_infrastructure.services_provider

            info_services = {}
            for key, service in self.services_provider().items():
                if hasattr(service, "info"):
                    info_services[key] = service.info()
                else:
                    raise TypeError(f"{key} must implement info")
            self.info["services"] = info_services
        if config_infrastructure.repositories_provider:
            self.repositories_provider = config_infrastructure.repositories_provider

            info_repositories = {}
            for key, repository in self.repositories_provider().items():
                if hasattr(repository, "info"):
                    info_repositories[key] = repository.info()
                else:
                    raise TypeError(f"{key} must implement info")
            self.info["repositories"] = info_repositories
        if config_infrastructure.event_manager_provider:
            self.event_manager_provider = config_infrastructure.event_manager_provider
            event_manager = self.event_manager_provider()
            if hasattr(event_manager, "info"):
                self.info["event_managers"] = event_manager.info()
            else:
                raise TypeError(f"Given event_manager must implement info")

    def start(self):
        self.application.start()

    def get_app(self):
        self.application.get_app()
