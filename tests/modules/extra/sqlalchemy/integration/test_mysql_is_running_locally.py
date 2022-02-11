import pytest

from petisco.extra.sqlalchemy.sql.mysql_is_running_locally import (
    mysql_is_running_locally,
)
from tests.modules.extra.decorators import testing_with_mysql


@pytest.mark.integration
@testing_with_mysql
def test_should_check_mysql_is_running_locally():
    assert mysql_is_running_locally()
