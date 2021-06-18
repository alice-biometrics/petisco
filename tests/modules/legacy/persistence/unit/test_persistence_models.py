import pytest

from petisco.legacy import PersistenceModels
from tests.modules.legacy.persistence.mother.model_filename_mother import (
    ModelFilenameMother,
)
from tests.modules.legacy.persistence.ymls.object.models import UserModel, ProductModel


@pytest.mark.unit
def test_should_load_from_filename_persistence_models_getting_models_names():
    filename = ModelFilenameMother.get("object/persistence.object.models.yml")
    persistence_model_names = PersistenceModels.from_filename(
        filename
    ).get_models_names()
    assert persistence_model_names == {
        "user": "tests.modules.legacy.persistence.ymls.object.models.UserModel",
        "product": "tests.modules.legacy.persistence.ymls.object.models.ProductModel",
    }


@pytest.mark.unit
def test_should_load_from_filename_persistence_models_getting_imported_models():
    filename = ModelFilenameMother.get("object/persistence.object.models.yml")
    persistence_models = PersistenceModels.from_filename(filename)
    persistence_models.import_models()
    models = persistence_models.get_imported_models()
    assert models.get("user").__module__ == UserModel.__module__
    assert models.get("product").__module__ == ProductModel.__module__
    assert models.get("user").__class__ == UserModel.__class__
    assert models.get("product").__class__ == ProductModel.__class__
