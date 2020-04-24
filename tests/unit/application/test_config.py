import pytest
import os

from petisco.application.config.config import Config


@pytest.fixture
def petisco_yml_path():
    return f"{os.path.dirname(os.path.abspath(__file__))}"


@pytest.mark.unit
def test_should_load_complete_petisco_yml(petisco_yml_path):

    filename = f"{petisco_yml_path}/ymls/petisco.all.yml"

    config = Config.from_filename(filename).unwrap()

    assert config.config_persistence.config_func is not None
    assert config.config_persistence.models is not None

    assert config.config_providers.services_provider_func is not None
    assert config.config_providers.repositories_provider_func is not None
