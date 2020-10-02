from typing import Callable, Dict

import pytest

from petisco.application.config.config import Config


@pytest.mark.end2end
def test_should_load_complete_petisco_yml(petisco_yml_path_end2end):

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"

    config = Config.from_filename(filename).unwrap()

    assert len(config.config_tasks.tasks.keys()) == 3

    assert isinstance(config.config_persistence.configs, Dict)
    assert isinstance(config.config_persistence.configs["petisco"].config, Callable)
    assert config.config_persistence.configs["petisco"].models is not None

    assert isinstance(config.config_providers.services_provider, Callable)
    assert isinstance(config.config_providers.repositories_provider, Callable)
    assert isinstance(config.config_notifier.provider, Callable)


@pytest.mark.end2end
def test_should_load_a_petisco_yml_with_no_events(petisco_yml_path_end2end):

    filename = f"{petisco_yml_path_end2end}/petisco.noevents.yml"

    config = Config.from_filename(filename).unwrap()

    assert isinstance(config.config_persistence.configs, Dict)
    assert isinstance(config.config_persistence.configs["petisco"].config, Callable)
    assert config.config_persistence.configs["petisco"].models is not None

    assert isinstance(config.config_providers.services_provider, Callable)
    assert isinstance(config.config_providers.repositories_provider, Callable)


@pytest.mark.end2end
def test_should_load_a_petisco_yml_with_events_no_subscribers(petisco_yml_path_end2end):

    filename = f"{petisco_yml_path_end2end}/petisco.events.nosubscribers.yml"

    config = Config.from_filename(filename).unwrap()

    assert isinstance(config.config_persistence.configs, Dict)
    assert isinstance(config.config_persistence.configs["petisco"].config, Callable)
    assert config.config_persistence.configs["petisco"].models is not None

    assert isinstance(config.config_providers.services_provider, Callable)
    assert isinstance(config.config_providers.repositories_provider, Callable)
