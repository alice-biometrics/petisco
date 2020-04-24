from typing import Optional

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string


@dataclass
class ConfigEventManager:
    event_manager_provider_func: Optional[str] = None
    publish_deploy_event: Optional[bool] = False
    event_topic: Optional[str] = None

    @staticmethod
    def from_dict(kdict):
        return ConfigEventManager(
            event_manager_provider_func=kdict.get("provider"),
            publish_deploy_event=kdict.get("publish_deploy_event", False),
            event_topic=kdict.get("event_topic"),
        )

    @property
    def event_manager_provider(self):
        return get_function_from_string(self.event_manager_provider_func)
