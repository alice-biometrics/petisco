import pytest

from petisco import PersistenceModels
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother
from tests.modules.persistence.ymls.object.models import UserModel, ProductModel


@pytest.mark.unit
def test_should_load_from_filename_persistence_models_getting_models_names():
    filename = ModelFilenameMother.get("object/persistence.object.models.yml")
    persistence_model_names = PersistenceModels.from_filename(
        filename
    ).get_models_names()
    assert persistence_model_names == {
        "user": "tests.modules.persistence.ymls.object.models.UserModel",
        "product": "tests.modules.persistence.ymls.object.models.ProductModel",
    }


@pytest.mark.unit
def test_should_load_from_filename_persistence_models_getting_imported_models():
    filename = ModelFilenameMother.get("object/persistence.object.models.yml")
    persistence_models = PersistenceModels.from_filename(filename).get_imported_models()
    assert persistence_models.get("user") == UserModel
    assert persistence_models.get("product") == ProductModel
