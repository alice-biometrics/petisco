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
    # assert "repositories" in petisco.info["elapsed_time"]
    # assert "services" in petisco.info["elapsed_time"]
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
def test_should_check_if_given_any_petisco_fixture_is_working_as_expected(
    given_any_petisco
):
    assert given_any_petisco._app_name == "petisco"
    assert given_any_petisco._app_version == "1.0.0"


@pytest.mark.end2end
def test_should_check_error_when_petisco_is_not_initialized():
    with pytest.raises(Exception) as excinfo:
        Petisco.get_instance()
        solutions_text = (
            f"\t Possible Solutions:\n"
            f"\t  * If you are testing and need any preconfigured Petisco, you can use the fixture given_any_petisco.\n"
            f"\t  * If you are testing and need specific preconfigured Petisco, you can create a fixture loading a petisco and then clearing.\n"
            f"\t  * If you are running a Petisco application, please review your loading process, petisco.yml is probably failing.\n"
        )
        assert solutions_text in str(excinfo.value)


@pytest.mark.end2end
def test_should_stop_petisco_without_configured_task(petisco_yml_path_end2end):

    Petisco.clear()

    filename = f"{petisco_yml_path_end2end}/../flask_app/petisco.notasks.yml"

    petisco = Petisco.from_filename(filename)

    petisco.stop()
    Petisco.clear()
