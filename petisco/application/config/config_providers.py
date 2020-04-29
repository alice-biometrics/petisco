from typing import Optional, Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


@dataclass
class ConfigProviders:
    config_dependencies: Optional[Callable] = None
    services_provider: Optional[Callable] = None
    repositories_provider: Optional[Callable] = None

    @staticmethod
    def from_dict(kdict):
        config_dependencies = (
            get_function_from_string(kdict.get("config_dependencies"))
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "providers:config_dependencies"),
            )
            .unwrap()
        )
        services_provider = (
            get_function_from_string(kdict.get("services_provider"))
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "providers:services_provider"),
            )
            .unwrap()
        )
        repositories_provider = (
            get_function_from_string(kdict.get("repositories_provider"))
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "providers:repositories_provider"),
            )
            .unwrap()
        )

        return ConfigProviders(
            config_dependencies=config_dependencies,
            services_provider=services_provider,
            repositories_provider=repositories_provider,
        )
