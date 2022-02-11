import pytest

from petisco.extra.rabbitmq import rabbitmq_is_running_locally
from tests.modules.extra.testing_decorators import testing_with_rabbitmq


@pytest.mark.integration
@testing_with_rabbitmq
def test_should_check_rabbitmq_is_running_locally():
    assert rabbitmq_is_running_locally()
