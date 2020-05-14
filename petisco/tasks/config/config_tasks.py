from typing import Optional, Dict

from dataclasses import dataclass

from petisco.tasks.config.config_tasks_job import ConfigTasksJob


@dataclass
class ConfigTasks:
    jobs: Optional[Dict[str, ConfigTasksJob]] = None

    @staticmethod
    def from_dict(kdict):
        if not kdict or not isinstance(kdict, dict):
            return ConfigTasks({})

        jobs = {}
        for key, config_job in kdict.items():
            jobs[key] = ConfigTasksJob.from_dict(config_job)

        return ConfigTasks(jobs)
