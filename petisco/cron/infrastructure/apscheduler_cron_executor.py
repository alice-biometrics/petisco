import atexit

from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.blocking import BlockingScheduler

from petisco.application.config.cron.config_cron import ConfigCron
from petisco.cron.domain.interface_cron_executor import CronExecutor
from apscheduler.schedulers.background import BackgroundScheduler


class APSchedulerCronExecutor(CronExecutor):
    def __init__(self, scheduler: BlockingScheduler = BackgroundScheduler()):
        self.scheduler = scheduler

    def start(self, config_cron: ConfigCron):
        for config_cron_job in config_cron.jobs.values():
            self.scheduler.add_job(
                func=config_cron_job.get_handler(),
                trigger="interval",
                seconds=config_cron_job.seconds,
            )

        try:
            self.scheduler.start()
            atexit.register(lambda: self.scheduler.shutdown())
        except SchedulerAlreadyRunningError:
            pass

    def stop(self):
        self.scheduler.shutdown()
