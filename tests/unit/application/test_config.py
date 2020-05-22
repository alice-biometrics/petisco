from typing import Callable

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

    assert len(config.config_tasks.tasks.keys()) == 3

    assert isinstance(config.config_persistence.config, Callable)
    assert config.config_persistence.models is not None

    assert isinstance(config.config_providers.services_provider, Callable)
    assert isinstance(config.config_providers.repositories_provider, Callable)
    assert isinstance(config.config_notifier.provider, Callable)


@pytest.mark.unit
def test_should_load_a_petisco_yml_with_no_events(petisco_yml_path):

    filename = f"{petisco_yml_path}/ymls/petisco.noevents.yml"

    config = Config.from_filename(filename).unwrap()

    assert isinstance(config.config_persistence.config, Callable)
    assert config.config_persistence.models is not None

    assert isinstance(config.config_providers.services_provider, Callable)
    assert isinstance(config.config_providers.repositories_provider, Callable)


@pytest.mark.unit
def test_should_load_a_petisco_yml_with_events_no_subscribers(petisco_yml_path):

    filename = f"{petisco_yml_path}/ymls/petisco.events.nosubscribers.yml"

    config = Config.from_filename(filename).unwrap()

    assert isinstance(config.config_persistence.config, Callable)
    assert config.config_persistence.models is not None

    assert isinstance(config.config_providers.services_provider, Callable)
    assert isinstance(config.config_providers.repositories_provider, Callable)
