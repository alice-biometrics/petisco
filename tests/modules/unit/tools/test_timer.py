import pytest
from meiga import Success
from meiga.assertions import assert_success

from petisco.tools.timer import timer


@pytest.mark.unit
def test_should_add_elapsed_time_to_results_when_use_timer_decorator():
    @timer
    def controller():
        return Success(({"message": "Ok"}, 200))

    result, elapsed_time = controller()

    assert_success(result)
    assert isinstance(elapsed_time, float)
