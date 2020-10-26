import importlib
import sys
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
        def _is_class_in_sqlalchemy_tables(class_model_name: str):
            # We need this to filter deletion in case of Model dependencies.
            # For instance, ClientConfigModel imports ClientModel on class model definition
            # It throws the following error:
            #  sqlalchemy.exc.InvalidRequestError: Table 'ClientConfig' is already defined for this MetaData instance.
            #  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
            # As a workaround, we only delete the module if it not exist in SQLAlchemy tables.
            from petisco.persistence.sqlalchemy.sqlalchemy_persistence import (
                SqlAlchemyPersistence,
            )

            is_in_tables = False
            for source in SqlAlchemyPersistence.get_instance().sources.values():
                Base = source.get("base")
                if not Base:
                    continue
                is_in_tables = class_model_name.replace("Model", "") in list(
                    Base.metadata.tables.keys()
                )
            return is_in_tables

        def _delete_module_if_already_imported(module_name: str, class_model_name: str):
            # Important. SqlAlchemy needs models to be imported
            # Base = SqlAlchemyPersistence.get_instance().sources["petisco"]["base"]
            # If module is already imported and Base has not tables, Tables won't be imported.
            # This, usually happens when start the application (e.g end2end tests)
            # e.g len(Base.metadata.tables) == 0
            # With this function we ensure that model can be imported to help SqlAlchemy loading models if is not imported yet
            if module_name in sys.modules and not _is_class_in_sqlalchemy_tables(
                class_model_name
            ):
                del sys.modules[module_name]

        def _import_database_models_func():
            for name, model_string in self.configs[persistence_entry].models.items():
                module_name, class_model_name = model_string.rsplit(".", 1)
                _delete_module_if_already_imported(module_name, class_model_name)
                importlib.import_module(module_name, class_model_name)

        return _import_database_models_func
