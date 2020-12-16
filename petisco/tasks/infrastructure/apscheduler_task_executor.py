import atexit
from datetime import datetime, timedelta

from apscheduler.schedulers import (
    SchedulerAlreadyRunningError,
    SchedulerNotRunningError,
)
from apscheduler.schedulers.blocking import BlockingScheduler

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from petisco.tasks.config.config_tasks import ConfigTasks
from petisco.tasks.domain.interface_task_executor import TaskExecutor


class APSchedulerTaskExecutor(TaskExecutor):
    def __init__(self, scheduler: BlockingScheduler = BackgroundScheduler()):
        self.scheduler = scheduler

    def start(self, config_tasks: ConfigTasks):
        for task in config_tasks.tasks.values():
            self._config_task(task)
        try:
            self.scheduler.start()
            atexit.register(lambda: self.stop())
        except SchedulerAlreadyRunningError:
            pass

    def _config_task(self, task):
        if task.type == "recurring":
            self._config_recurring_task(task)
        elif task.type == "scheduled":
            self._config_scheduled_task(task)
        elif task.type == "cron":
            self._config_cron_task(task)
        else:
            self._config_instant_task(task)

    def _config_recurring_task(self, task):
        now = datetime.utcnow()
        start_date = now + timedelta(0, task.run_in)
        self.scheduler.add_job(
            func=task.get_handler(),
            start_date=start_date,
            trigger="interval",
            seconds=task.interval,
        )

    def _config_scheduled_task(self, task):
        now = datetime.utcnow()
        start_date = now + timedelta(0, task.run_in)
        self.scheduler.add_job(
            func=task.get_handler(), trigger="date", run_date=start_date
        )

    def _config_cron_task(self, task):
        self.scheduler.add_job(
            func=task.get_handler(), trigger=CronTrigger.from_crontab(task.every)
        )

    def _config_instant_task(self, task):
        self.scheduler.add_job(func=task.get_handler())

    def stop(self):
        try:
            self.scheduler.shutdown()
        except SchedulerNotRunningError:
            pass
