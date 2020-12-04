import pytest

from petisco import Persistence, FakeDatabase
from tests.modules.persistence.mother.model_filename_mother import ModelFilenameMother


@pytest.mark.unit
def test_should_execute_lifecycle_of_persistence_with_fake_database():
    filename = ModelFilenameMother.get("object/persistence.object.models.yml")
    database = FakeDatabase(name="fake", model_filename=filename)

    persistence = Persistence()
    persistence.add(database)
    assert ["fake"] == persistence.get_available_databases()
    assert ["user", "product"] == persistence.get_available_models_for_database("fake")
    assert (
        "tests.modules.persistence.ymls.object.models.UserModel"
        == persistence.get_model("fake", "user")
    )
    persistence.remove("fake")
    assert [] == persistence.get_available_databases()
    with pytest.raises(IndexError):
        persistence.get_model("fake", "user")

    persistence.create()
    persistence.delete()
    Persistence.clear()
