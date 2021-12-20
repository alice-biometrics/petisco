import importlib
import os
import sys
import traceback
from typing import Any, Dict

import yaml
from yaml.parser import ParserError, ScannerError


class PersistenceModels:
    def __init__(self, models: Dict[str, Any]):
        self.models = models
        self.imported_models = {}

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
        self.imported_models = self.import_database_models()

        # self.imported_models = {}
        # for name, model_string in self.models.items():
        #     mod_name, model_name = model_string.rsplit(".", 1)
        #     mod = importlib.import_module(mod_name)
        #     self.imported_models[name] = getattr(mod, model_name)

    def import_database_models(self):
        def _is_class_in_sqlalchemy_tables(class_model_name: str):
            # We need this to filter deletion in case of Model dependencies.
            # For instance, ClientConfigModel imports ClientModel on class model definition
            # It throws the following error:
            #  sqlalchemy.exc.InvalidRequestError: Table 'ClientConfig' is already defined for this MetaData instance.
            #  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
            # As a workaround, we only delete the module if it not exist in SQLAlchemy tables.

            from petisco.base.domain.persistence.persistence import Persistence

            is_in_tables = False
            for database in Persistence.get_databases():
                if not hasattr(database, "get_base"):
                    continue
                Base = database.get_base()
                if not Base:
                    continue
                is_in_tables = class_model_name.replace("Model", "") in list(
                    Base.metadata.tables.keys()
                )
            return is_in_tables

        def _delete_module_if_already_imported(module_name: str, class_model_name: str):
            # Important. SqlAlchemy needs models to be imported
            # Base = Persistence.get_base("petisco")
            # If module is already imported and Base has not tables, Tables won't be imported.
            # This, usually happens when start the application (e.g end2end tests)
            # e.g len(Base.metadata.tables) == 0
            # With this function we ensure that model can be imported to help SqlAlchemy loading models if is not imported yet
            if module_name in sys.modules and not _is_class_in_sqlalchemy_tables(
                class_model_name
            ):
                del sys.modules[module_name]

        def _import_database_models_func():
            imported_models = {}
            for name, model_string in self.models.items():
                module_name, class_model_name = model_string.rsplit(".", 1)
                _delete_module_if_already_imported(module_name, class_model_name)
                module_name = importlib.import_module(module_name, class_model_name)
                imported_models[name] = getattr(module_name, class_model_name)
            return imported_models

        return _import_database_models_func()

    def get_imported_models(self):
        return self.imported_models
