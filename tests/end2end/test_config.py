import pytest

from petisco.application.config.config import Config


@pytest.mark.end2end
def test_should_load_complete_petisco_yml(petisco_yml_path_end2end):

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"

    config = Config.from_filename(filename).unwrap()

    assert len(config.config_tasks.tasks.keys()) == 3
