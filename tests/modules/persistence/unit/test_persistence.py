import pytest

from petisco import Persistence, FakeDatabase


@pytest.mark.unit
def test_should_execute_lifecycle_of_persistence_with_fake_database():
    persistence = Persistence()
    persistence.add(FakeDatabase(name="fake", models={"model1": "model-content-1"}))
    assert ["fake"] == persistence.get_available_databases()
    assert ["model1"] == persistence.get_available_models_for_database("fake")
    assert "model-content-1" == persistence.get_model("fake", "model1")
    persistence.remove("fake")
    assert [] == persistence.get_available_databases()
    with pytest.raises(IndexError):
        persistence.get_model("fake", "model1")

    persistence.create()
    persistence.delete()
