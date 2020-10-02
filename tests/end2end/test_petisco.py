from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

import pytest
import os

from petisco import Petisco


@pytest.mark.end2end
def test_should_load_petisco_from_yml(petisco_yml_path_end2end, given_petisco_version):

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"

    expected_petisco_info = {
        "app_name": "toy-app",
        "app_version": "1.0.0",
        "petisco_version": given_petisco_version,
        "environment": None,
        "services": {"sum": {"name": "SumExecutor"}},
        "repositories": {
            "user": {"name": "SqlUserRepository"},
            "users_count": {"name": "SqlUsersCountRepository"},
        },
        "event_publisher": {"name": "NotImplementedEventPublisher"},
        "event_subscriber": {"name": "NotImplementedEventSubscriber"},
        "tasks": {
            "recurring-task": {"type": "recurring", "run_in": 0.0, "interval": 10.0},
            "scheduled-task": {"type": "scheduled", "run_in": 10.0},
            "instant-task": {"type": "instant", "run_in": 0.0},
        },
    }

    petisco = Petisco.from_filename(filename)
    petisco.load_services_and_repositories()

    assert "elapsed_time" in petisco.info
    assert "load_repositories" in petisco.info["elapsed_time"]
    assert "load_services" in petisco.info["elapsed_time"]
    petisco.info.pop("elapsed_time")
    assert petisco.info == expected_petisco_info
    Petisco.clear()


@pytest.mark.end2end
def test_should_load_petisco_from_yml_and_schedule_tasks(petisco_yml_path_end2end):

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"

    petisco = Petisco.from_filename(filename)

    petisco._schedule_tasks()

    Petisco.clear()


@pytest.mark.end2end
@pytest.mark.parametrize(
    "logging_level, logging_level_num",
    [
        ("DEBUG", DEBUG),
        ("INFO", INFO),
        ("WARNING", WARNING),
        ("ERROR", ERROR),
        ("CRITICAL", CRITICAL),
    ],
)
def test_should_load_petisco_from_yml_and_check_logger_level(
    logging_level, logging_level_num, petisco_yml_path_end2end
):

    Petisco.clear()
    os.environ["PETISCO_LOGGING_LEVEL"] = logging_level

    filename = f"{petisco_yml_path_end2end}/petisco.all.withlogging.yml"

    petisco = Petisco.from_filename(filename)

    assert hasattr(petisco.get_logger(), "logging_level")
    assert petisco.get_logger().logging_level == logging_level
    assert petisco.get_logger().logger.level == logging_level_num

    del os.environ["PETISCO_LOGGING_LEVEL"]
    Petisco.clear()


@pytest.mark.end2end
def test_should_raise_exception_if_repository_not_exist(petisco_yml_path_end2end):

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"

    petisco = Petisco.from_filename(filename)
    with pytest.raises(ValueError):
        petisco.get_repository("repo")

    Petisco.clear()


@pytest.mark.end2end
def test_should_raise_exception_if_service_not_exist(petisco_yml_path_end2end):

    filename = f"{petisco_yml_path_end2end}/petisco.all.yml"

    petisco = Petisco.from_filename(filename)
    with pytest.raises(ValueError):
        petisco.get_service("repo")

    Petisco.clear()


@pytest.mark.end2end
def test_should_check_if_given_any_petisco_fixture_is_working_as_expected(
    given_any_petisco
):
    assert given_any_petisco.app_name == "petisco"
    assert given_any_petisco.app_version == "1.0.0"
