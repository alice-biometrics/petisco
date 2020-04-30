from typing import Optional, Dict

from dataclasses import dataclass

from petisco.application.config.cron.config_cron_job import ConfigCronJob


@dataclass
class ConfigCron:
    jobs: Optional[Dict[str, ConfigCronJob]] = None

    @staticmethod
    def from_dict(kdict):
        if not kdict or not isinstance(kdict, dict):
            return ConfigCron({})

        jobs = {}
        for key, config_job in kdict.items():
            jobs[key] = ConfigCronJob.from_dict(config_job)

        return ConfigCron(jobs)
