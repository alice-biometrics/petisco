import importlib
from typing import Optional, Dict, Any, Callable

from dataclasses import dataclass

from petisco.application.config.get_funtion_from_string import get_function_from_string
from petisco.application.config.raise_petisco_config_error import (
    raise_petisco_config_exception,
)


@dataclass
class ConfigPersistence:
    config: Optional[Callable] = None
    models: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(kdict):
        if not kdict or not isinstance(kdict, dict):
            return ConfigPersistence()
        config = (
            get_function_from_string(kdict.get("config"))
            .handle(
                on_failure=raise_petisco_config_exception,
                failure_args=(kdict, "persistence:config"),
            )
            .unwrap()
        )
        return ConfigPersistence(config=config, models=kdict.get("models"))

    def get_models(self):
        loaded_models = {}
        for name, model_string in self.models.items():
            mod_name, model_name = model_string.rsplit(".", 1)
            mod = importlib.import_module(mod_name)
            loaded_models[name] = getattr(mod, model_name)
        return loaded_models

    def get_import_database_models_func(self):
        def _import_database_models_func():
            for name, model_string in self.models.items():
                mod_name, model_name = model_string.rsplit(".", 1)
                __import__(mod_name, fromlist=[model_name])

        return _import_database_models_func
