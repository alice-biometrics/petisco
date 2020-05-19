import pytest
import os

from petisco import Petisco


@pytest.fixture
def petisco_yml_path():
    return f"{os.path.dirname(os.path.abspath(__file__))}"


@pytest.mark.unit
def test_should_load_petisco_from_yml(petisco_yml_path, given_petisco_version):

    filename = f"{petisco_yml_path}/ymls/petisco.all.yml"
    expected_petisco_info = {
        "app_name": "toy-app",
        "app_version": "1.0.0",
        "petisco_version": given_petisco_version,
        "services": {"sum": {"name": "SumService"}},
        "repositories": {"user": {"name": "SqlUserRepository"}},
        "event_publisher": {"name": "NotImplementedEventPublisher"},
        "event_subscriber": {"name": "NotImplementedEventSubscriber"},
        "tasks": {
            "recurring-task": {"type": "recurring", "run_in": 5.0, "interval": 10.0},
            "scheduled-task": {"type": "scheduled", "run_in": 10.0},
            "instant-task": {"type": "instant"},
        },
    }

    petisco = Petisco.from_filename(filename)

    assert petisco.info == expected_petisco_info


@pytest.mark.unit
def test_should_schedule_tasks(petisco_yml_path):

    filename = f"{petisco_yml_path}/ymls/petisco.all.yml"

    petisco = Petisco.from_filename(filename)

    petisco._schedule_tasks()
