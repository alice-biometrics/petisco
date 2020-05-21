import os
import traceback
from typing import Dict, Any, List

import yaml
from meiga import Result, Error, Failure, Success
from meiga.decorators import meiga
from yaml.parser import ParserError, ScannerError

from petisco.application.config.config_persistence import ConfigPersistence
from petisco.application.config.config_providers import ConfigProviders
from petisco.notifier.config.config_notifier import ConfigNotifier
from petisco.notifier.domain.interface_notifier import INotifier
from petisco.tasks.config.config_tasks import ConfigTasks
from petisco.frameworks.interface_application import IApplication
from petisco.logger.interface_logger import ILogger
from petisco.logger.logging_based_logger import LoggingBasedLogger
from petisco.application.config.events.config_events import ConfigEvents
from petisco.application.config.config_file_not_found_error import (
    ConfigFileNotFoundError,
)
from petisco.application.config.config_file_not_valid_error import (
    ConfigFileNotValidError,
)
from petisco.application.config.config_framework import ConfigFramework
from petisco.application.config.config_logger import ConfigLogger
from petisco.logger.not_implemented_logger import NotImplementedLogger


class Config:
    def __init__(
        self,
        app_name: str,
        app_version: str,
        petisco_yml_folder: str = None,
        config_tasks: ConfigTasks = None,
        config_framework: ConfigFramework = None,
        config_logger: ConfigLogger = None,
        config_notifier: ConfigNotifier = None,
        config_persistence: ConfigPersistence = None,
        config_providers: ConfigProviders = None,
        config_events: ConfigEvents = None,
        options: Dict = None,
    ):
        self.app_name = app_name
        self.app_version = app_version
        self.petisco_yml_folder = petisco_yml_folder
        self.config_tasks = config_tasks
        self.config_framework = config_framework
        self.config_logger = config_logger
        self.config_notifier = config_notifier
        self.config_persistence = config_persistence
        self.config_providers = config_providers
        self.config_events = config_events
        self.options = options

    @staticmethod
    @meiga
    def from_filename(filename: str) -> Result[Any, Error]:
        if not os.path.isfile(filename):
            return Failure(ConfigFileNotFoundError(filename))
        try:
            petisco_yml_folder = os.path.dirname(filename)
            with open(filename) as file:
                petisco_dict = yaml.load(file, Loader=yaml.FullLoader)
                petisco_dict["petisco_yml_folder"] = petisco_yml_folder
                config = Config.from_dict(petisco_dict).unwrap_or_return()
                return Success(config)
        except (ParserError, ScannerError) as e:
            message = f"Error loading {filename} file: {repr(e.__class__)} {e} | {traceback.format_exc()}"
            return Failure(ConfigFileNotValidError(message))

    @staticmethod
    @meiga
    def from_dict(yaml_dict: Dict) -> Result[Any, Error]:
        petisco_yml_folder = yaml_dict.get("petisco_yml_folder")
        app_config = yaml_dict.get("app")
        app_name = app_config.get("name")
        app_version = Config.get_version(
            petisco_yml_folder, app_config.get("version")
        ).unwrap_or_return()

        config_tasks = ConfigTasks.from_dict(yaml_dict.get("tasks"))

        config_framework = ConfigFramework.from_dict(yaml_dict.get("framework"))

        config_logger = Config.get_config_logger(
            yaml_dict.get("logger")
        ).unwrap_or_return()

        config_notifier = ConfigNotifier.from_dict(yaml_dict.get("notifier"))

        config_persistence = ConfigPersistence.from_dict(yaml_dict.get("persistence"))

        config_providers = ConfigProviders.from_dict(yaml_dict.get("providers"))

        config_events = ConfigEvents.from_dict(yaml_dict.get("events"))

        options = app_config.get("options")

        return Success(
            Config(
                petisco_yml_folder=petisco_yml_folder,
                app_name=app_name,
                app_version=app_version,
                config_tasks=config_tasks,
                config_framework=config_framework,
                config_logger=config_logger,
                config_notifier=config_notifier,
                config_providers=config_providers,
                config_events=config_events,
                config_persistence=config_persistence,
                options=options,
            )
        )

    @staticmethod
    def get_version(petisco_yml_folder, config_version) -> Result[str, Error]:
        if isinstance(config_version, str):
            return Success(config_version)
        else:
            version_filename = config_version.get("from_file")
            if not version_filename:
                Failure(
                    ConfigFileNotValidError(
                        "If you don't specify the version directly, you must associate a file with from_file key"
                    )
                )

            version_filename = f"{petisco_yml_folder}/{version_filename}"
            if not os.path.isfile(version_filename):
                return Failure(
                    ConfigFileNotValidError(
                        f"Version from_file does not exist ({version_filename})"
                    )
                )
            version = open(version_filename, "r").read()
            return Success(version.rstrip("\n"))

    @staticmethod
    def get_config_logger(config_logger_dict: Dict) -> Result[ConfigLogger, Error]:

        if not config_logger_dict:
            return Success(ConfigLogger())
        else:
            return Success(ConfigLogger.from_dict(config_logger_dict))

    def get_logger(self) -> ILogger:
        if not self.config_logger or self.config_logger.selected_logger != "logging":
            return NotImplementedLogger()
        else:
            return LoggingBasedLogger(
                logger_name=self.config_logger.name,
                format=self.config_logger.format,
                config=self.config_logger.config,
            )

    def get_notifier(self) -> INotifier:
        return self.config_notifier.provider()

    def get_application(self) -> IApplication:
        if not self.config_framework:
            return None

        if self.config_framework.selected_framework != "flask":
            raise TypeError(
                f"Selected framework ({self.config_framework.selected_framework}) is not allowed. Try with flask."
            )
        else:
            if not self.config_framework.port_env:
                port = self.config_framework.port
            else:
                port = (
                    self.config_framework.port
                    if not os.environ.get(self.config_framework.port_env)
                    else os.environ.get(self.config_framework.port_env)
                )

            from petisco.frameworks.flask.application.flask_application import (
                FlaskApplication,
            )

            conf_file_split: List = self.config_framework.config_file.split("/")

            if len(conf_file_split) == 1:
                swagger_dir = self.petisco_yml_folder
                config_file = conf_file_split[0]
            else:
                swagger_dir, config_file = conf_file_split

            return FlaskApplication(
                application_name=self.app_name,
                swagger_dir=swagger_dir,
                config_file=config_file,
                port=port,
            )
