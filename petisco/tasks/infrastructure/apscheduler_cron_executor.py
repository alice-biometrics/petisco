import atexit

from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.blocking import BlockingScheduler

from apscheduler.schedulers.background import BackgroundScheduler

from petisco.tasks.config.config_tasks import ConfigTasks
from petisco.tasks.domain.interface_task_executor import TaskExecutor


class APSchedulerTaskExecutor(TaskExecutor):
    def __init__(self, scheduler: BlockingScheduler = BackgroundScheduler()):
        self.scheduler = scheduler

    def start(self, config_tasks: ConfigTasks):
        for config_tasks_job in config_tasks.jobs.values():
            self.scheduler.add_job(
                func=config_tasks_job.get_handler(),
                trigger="interval",
                seconds=config_tasks_job.seconds,
            )

        try:
            self.scheduler.start()
            atexit.register(lambda: self.scheduler.shutdown())
        except SchedulerAlreadyRunningError:
            pass

    def stop(self):
        self.scheduler.shutdown()
