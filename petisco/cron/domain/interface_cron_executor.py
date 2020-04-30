from abc import ABCMeta, abstractmethod

from petisco.application.config.cron.config_cron import ConfigCron


class CronExecutor:

    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, config_cron: ConfigCron):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
