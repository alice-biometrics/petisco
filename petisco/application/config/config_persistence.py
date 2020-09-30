import importlib
from typing import Optional, Dict, Any, Callable, List

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


@dataclass
class SingleConfigPersistence:
    type: str
    config: Optional[Callable] = None
    models: Optional[Dict[str, Any]] = None


@dataclass
class ConfigPersistence:

    configs: Optional[Dict[str, SingleConfigPersistence]] = None

    @staticmethod
    def from_dict(kdict):
        if not kdict or not isinstance(kdict, List):
            return ConfigPersistence()
        configs = {}
        for entry in kdict:
            config = (
                get_function_from_string(entry.get("config"))
                .handle(
                    on_failure=raise_petisco_config_exception,
                    failure_args=(entry, "persistence:config"),
                )
                .unwrap()
            )
            configs[entry["name"]] = SingleConfigPersistence(
                type=entry["type"], config=config, models=entry.get("models")
            )
        return ConfigPersistence(configs=configs)

    def get_models(self, persistence_entry):
        loaded_models = {}
        for name, model_string in self.configs[persistence_entry].models.items():
            mod_name, model_name = model_string.rsplit(".", 1)
            mod = importlib.import_module(mod_name)
            loaded_models[name] = getattr(mod, model_name)
        return loaded_models

    def get_import_database_models_func(self, persistence_entry):
        def _import_database_models_func():
            for name, model_string in self.configs[persistence_entry].models.items():
                mod_name, model_name = model_string.rsplit(".", 1)
                __import__(mod_name, fromlist=[model_name])

        return _import_database_models_func
