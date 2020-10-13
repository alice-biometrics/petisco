from petisco.tasks.config.config_tasks import ConfigTasks
from petisco.tasks.domain.interface_task_executor import TaskExecutor


class NotImplementedTaskExecutor(TaskExecutor):
    def start(self, config_tasks: ConfigTasks):
        pass

    def stop(self):
        pass
