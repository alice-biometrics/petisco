import pytest

from petisco.extra.elastic.elastic_is_running_locally import elastic_is_running_locally
from tests.modules.extra.testing_decorators import testing_with_elastic


@pytest.mark.integration
@testing_with_elastic
def test_should_check_elastic_is_running_locally():
    assert elastic_is_running_locally()
