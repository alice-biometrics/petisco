import pytest
from meiga.assertions import assert_success

from petisco.domain.aggregate_roots.info_id import InfoId


@pytest.mark.unit
def test_should_check_info_id_to_result_method(given_any_info_id):

    info_id = given_any_info_id

    assert_success(info_id.to_result(), value_is_instance_of=InfoId)
