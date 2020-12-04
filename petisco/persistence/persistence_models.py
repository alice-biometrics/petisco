import importlib
import os
import traceback
from typing import Dict, Any

import yaml
from yaml.parser import ParserError, ScannerError


class PersistenceModels:
    def __init__(self, models: Dict[str, Any]):
        self.models = models

    @staticmethod
    def from_filename(filename: str):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"PersistenceModels ({filename} not found)")
        try:
            with open(filename) as file:
                petisco_dict = yaml.load(file, Loader=yaml.FullLoader)
                models = petisco_dict.get("models")
                return PersistenceModels(models)
        except (ParserError, ScannerError) as e:
            message = f"Error loading {filename} file: {repr(e.__class__)} {e} | {traceback.format_exc()}"
            raise RuntimeError(message)

    def get_models_names(self):
        return self.models

    def import_models(self):
        for name, model_string in self.models.items():
            mod_name, model_name = model_string.rsplit(".", 1)
            importlib.import_module(mod_name)

    def get_imported_models(self):
        imported_models = {}
        for name, model_string in self.models.items():
            mod_name, model_name = model_string.rsplit(".", 1)
            mod = importlib.import_module(mod_name)
            imported_models[name] = getattr(mod, model_name)
        return imported_models
