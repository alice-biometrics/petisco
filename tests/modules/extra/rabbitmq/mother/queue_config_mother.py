from petisco.extra.rabbitmq import SpecificQueueConfig
from petisco.extra.rabbitmq.shared.queue_config import QueueConfig


class QueueConfigMother:
    @staticmethod
    def default():
        return QueueConfig.default()

    @staticmethod
    def with_ttl_10():
        return QueueConfig.default(default_retry_ttl=10, default_main_ttl=10)

    @staticmethod
    def with_specific_queue_config(
        specific_queue_config: SpecificQueueConfig,
        default_retry_ttl: int,
        default_main_ttl: int,
    ):
        return QueueConfig(
            default_retry_ttl=default_retry_ttl,
            default_main_ttl=default_main_ttl,
            specific_queue_configs={"specific": specific_queue_config},
        )
