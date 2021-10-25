from datetime import datetime

import pytest

from petisco.application.deploy_checker import DeployChecker


@pytest.mark.unit
@pytest.mark.parametrize("courtesy_minutes", [16, 60])
def test_deploy_checker_should_check_is_recently_deployed(courtesy_minutes):

    deploy_time = "2021-10-25 09:00:00+00:00"
    now_time = datetime(year=2021, month=10, day=25, hour=9, minute=15, second=0)

    checker = DeployChecker(deploy_time=deploy_time, courtesy_minutes=courtesy_minutes)

    assert checker.was_recently_deployed(now_time) is True
    assert checker.get_deploy_time() == deploy_time


@pytest.mark.unit
def test_deploy_checker_should_check_is_not_recently_deployed():

    deploy_time = "2021-10-25 09:00:00+00:00"
    now_time = datetime(year=2021, month=10, day=25, hour=10, minute=10, second=0)
    courtesy_minutes = 60

    checker = DeployChecker(deploy_time=deploy_time, courtesy_minutes=courtesy_minutes)

    assert checker.was_recently_deployed(now_time) is False
    assert checker.get_deploy_time() == deploy_time
