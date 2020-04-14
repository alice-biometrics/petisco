from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from petisco.application.config.get_funtion_from_string import get_function_from_string


@dataclass_json
@dataclass
class ConfigInfrastructure:
    config_dependencies_func: Optional[str] = None
    services_provider_func: Optional[str] = None
    repositories_provider_func: Optional[str] = None
    event_manager_provider_func: Optional[str] = None
    publish_deploy_event_func: Optional[bool] = False
    event_topic: Optional[str] = None

    @property
    def config_dependencies(self):
        return get_function_from_string(self.config_dependencies_func)

    @property
    def config_persistence(self):
        return get_function_from_string(self.config_persistence_func)

    @property
    def services_provider(self):
        return get_function_from_string(self.services_provider_func)

    @property
    def repositories_provider(self):
        return get_function_from_string(self.repositories_provider_func)

    @property
    def event_manager_provider(self):
        return get_function_from_string(self.event_manager_provider_func)
