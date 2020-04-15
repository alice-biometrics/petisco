import importlib
from typing import Optional, Dict, Any

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from petisco.application.config.get_funtion_from_string import get_function_from_string


@dataclass_json
@dataclass
class ConfigPersistence:
    config_func: Optional[str] = None
    models: Optional[Dict[str, Any]] = None

    @property
    def config(self):
        return get_function_from_string(self.config_func)

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
