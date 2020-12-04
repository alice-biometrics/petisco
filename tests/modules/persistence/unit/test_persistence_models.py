import pytest

from petisco import PersistenceModels
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother


@pytest.mark.unit
def test_should_load_from_parser():
    filename = ModelFilenameMother.get("object/persistence.object.models.yml")
    persistence_models = PersistenceModels.from_filename(filename).get_models_names()
    assert persistence_models == {
        "user": "tests.modules.persistence.ymls.object.models.UserModel",
        "product": "tests.modules.persistence.ymls.object.models.ProductModel",
    }
