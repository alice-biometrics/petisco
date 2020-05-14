import atexit
from datetime import datetime, timedelta

from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.blocking import BlockingScheduler

from apscheduler.schedulers.background import BackgroundScheduler

from petisco.tasks.config.config_tasks import ConfigTasks
from petisco.tasks.domain.interface_task_executor import TaskExecutor


class APSchedulerTaskExecutor(TaskExecutor):
    def __init__(self, scheduler: BlockingScheduler = BackgroundScheduler()):
        self.scheduler = scheduler

    def start(self, config_tasks: ConfigTasks):
        for task in config_tasks.tasks.values():
            if task.cron_interval:
                self._config_recurring_task(task)
            else:
                if task.run_in:
                    self._config_scheduled_task(task)
                else:
                    self._config_instant_task(task)
        try:
            self.scheduler.start()
            atexit.register(lambda: self.scheduler.shutdown())
        except SchedulerAlreadyRunningError:
            pass

    def _config_recurring_task(self, task):
        self.scheduler.add_job(
            func=task.get_handler(), trigger="interval", seconds=task.cron_interval
        )

    def _config_scheduled_task(self, task):
        now = datetime.utcnow()
        start_date = now + timedelta(0, task.run_in)
        self.scheduler.add_job(
            func=task.get_handler(), trigger="date", run_date=start_date.date()
        )

    def _config_instant_task(self, task):
        self.scheduler.add_job(func=task.get_handler())

    def stop(self):
        self.scheduler.shutdown()
