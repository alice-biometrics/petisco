from typing import List

from petisco.base.domain.persistence.interface_database import Database
from petisco.base.domain.persistence.persistence_models import PersistenceModels


class FakeDatabase(Database):
    def __init__(self, name: str, model_filename: str):
        models = PersistenceModels.from_filename(model_filename).get_models_names()
        super().__init__(name, models=models)

    def create(self):
        pass

    def delete(self):
        pass

    def clear_data(self):
        pass

    def get_model(self, model_name: str):
        model = self.models.get(model_name)
        if not model:
            raise IndexError(
                f'Model "{model_name}" is not available for "{self.name}" database'
            )
        return model

    def get_model_names(self) -> List[str]:
        return list(self.models.keys())
