from petisco.legacy.tasks.config.config_tasks import ConfigTasks
from petisco.legacy.tasks.domain.interface_task_executor import TaskExecutor


class NotImplementedTaskExecutor(TaskExecutor):
    def start(self, config_tasks: ConfigTasks):
        pass

    def stop(self):
        pass
