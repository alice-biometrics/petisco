from typing import List, Dict

from petisco.persistence.interface_database import IDatabase


class FakeDatabase(IDatabase):
    def __init__(self, name: str, models: Dict = None):
        super().__init__(name, models=models)

    def create(self):
        pass

    def delete(self):
        pass

    def get_model(self, model_name: str):
        model = self.models.get(model_name)
        if not model:
            raise IndexError(
                f'Model "{model_name}" is not available for "{self.name}" databade'
            )
        return model

    def get_model_names(self) -> List[str]:
        return list(self.models.keys())
