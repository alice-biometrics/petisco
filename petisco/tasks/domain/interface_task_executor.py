from abc import ABCMeta, abstractmethod

from petisco.tasks.config.config_tasks import ConfigTasks


class TaskExecutor:

    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, config_tasks: ConfigTasks):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
