from typing import Optional

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string


@dataclass
class ConfigProviders:
    config_dependencies_func: Optional[str] = None
    services_provider_func: Optional[str] = None
    repositories_provider_func: Optional[str] = None

    @staticmethod
    def from_dict(kdict):
        return ConfigProviders(
            config_dependencies_func=kdict.get("config_dependencies"),
            services_provider_func=kdict.get("services_provider"),
            repositories_provider_func=kdict.get("repositories_provider"),
        )

    @property
    def config_dependencies(self):
        return get_function_from_string(self.config_dependencies_func)

    @property
    def services_provider(self):
        return get_function_from_string(self.services_provider_func)

    @property
    def repositories_provider(self):
        return get_function_from_string(self.repositories_provider_func)
