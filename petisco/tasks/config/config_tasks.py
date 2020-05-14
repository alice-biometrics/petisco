from typing import Optional, Dict

from dataclasses import dataclass

from petisco.tasks.config.config_task import ConfigTask


@dataclass
class ConfigTasks:
    tasks: Optional[Dict[str, ConfigTask]] = None

    @staticmethod
    def from_dict(kdict):
        if not kdict or not isinstance(kdict, dict):
            return ConfigTasks({})

        tasks = {}
        for key, config_task in kdict.items():
            tasks[key] = ConfigTask.from_dict(config_task)

        return ConfigTasks(tasks)
