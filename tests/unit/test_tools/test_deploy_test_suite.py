import pytest

from meiga import Result, isSuccess
from meiga.decorators import meiga

from petisco.test_tools import deploy_test, DeployTestBase, DeployTestsExecutor


@deploy_test
class FirstDeployTest(DeployTestBase):
    @meiga
    def execute(self, verbose: bool = False) -> Result:
        return isSuccess


@deploy_test
class SecondDeployTest(DeployTestBase):
    @meiga
    def execute(self, verbose: bool = False) -> Result:
        return isSuccess


@pytest.mark.unit
def test_should_check_available_deploy_tests():
    assert len(DeployTestsExecutor.get_available_tests()) == 2


@pytest.mark.unit
def test_should_execute_deploy_tests():

    deploy_test_executor = DeployTestsExecutor(verbose=True)

    is_success = deploy_test_executor.execute()

    assert is_success


@pytest.mark.unit
def test_should_execute_deploy_tests_selecting_tests():
    selected_test = "FirstDeployTest"

    deploy_test_executor = DeployTestsExecutor(verbose=True)

    is_success = deploy_test_executor.execute(selected_test=selected_test)

    assert is_success
