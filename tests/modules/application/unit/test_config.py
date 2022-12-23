import pytest

from petisco.application.config.events.config_events import ConfigEvents


@pytest.mark.unit
def test_should_instantiate():
    config_events = ConfigEvents()
