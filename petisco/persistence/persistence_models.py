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
