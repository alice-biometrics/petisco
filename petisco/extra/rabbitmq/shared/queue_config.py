from typing import Dict

from petisco.extra.rabbitmq.shared.specific_queue_config import SpecificQueueConfig


class QueueConfig:
    @staticmethod
    def from_dict(
        specific_queue_configs_dict: dict, default_retry_ttl: int, default_main_ttl: int
    ):
        specific_queue_configs = {}
        for key, config_dict in specific_queue_configs_dict.items():
            specific_queue_configs[key] = SpecificQueueConfig.from_dict(
                config_dict, default_retry_ttl, default_main_ttl
            )

        return QueueConfig(
            default_retry_ttl=default_retry_ttl,
            default_main_ttl=default_main_ttl,
            specific_queue_configs=specific_queue_configs,
        )

    @staticmethod
    def default(default_retry_ttl: int = 5000, default_main_ttl: int = 5000):
        return QueueConfig(
            default_retry_ttl=default_retry_ttl,
            default_main_ttl=default_main_ttl,
            specific_queue_configs={},
        )

    def __init__(
        self,
        default_retry_ttl: int,
        default_main_ttl: int,
        specific_queue_configs: Dict[str, SpecificQueueConfig],
    ):
        self.default_retry_ttl = default_retry_ttl
        self.default_main_ttl = default_main_ttl
        self.specific_queue_configs = specific_queue_configs

    def info(self) -> dict:
        return {
            name: specific_config.info()
            for name, specific_config in self.specific_queue_configs.items()
        }

    def get_retry_ttl(self, queue_name: str):
        for queue_config in self.specific_queue_configs.values():
            if queue_config.has_specific_config(queue_name):
                return queue_config.get_retry_ttl()
        return self.default_retry_ttl

    def get_main_ttl(self, queue_name: str):
        for queue_config in self.specific_queue_configs.values():
            if queue_config.has_specific_config(queue_name):
                return queue_config.get_main_ttl()
        return self.default_main_ttl
