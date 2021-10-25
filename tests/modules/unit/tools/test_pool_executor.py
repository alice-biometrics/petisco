import pytest
from meiga import Success, Result, Error, isFailure

from petisco import Executable, PoolExecutor


@pytest.mark.unit
@pytest.mark.parametrize(
    "use_multi_threading,unwrap_results,expected_result",
    [
        (True, True, [3, 4, 2, 10]),
        (False, True, [3, 4, 2, 10]),
        (True, False, [Success(3), Success(4), Success(2), Success(10)]),
        (False, False, [Success(3), Success(4), Success(2), Success(10)]),
    ],
)
def test_pool_executor_should_execute_several_executables(
    use_multi_threading, unwrap_results, expected_result
):
    def sum(param_1, param_2) -> Result[int, Error]:
        return Success(param_1 + param_2)

    def mul(param_1, param_2) -> Result[int, Error]:
        return Success(param_1 * param_2)

    executables = [
        Executable(func=sum, args=(1, 2)),
        Executable(func=sum, args=(2, 2)),
        Executable(func=mul, args=(1, 2)),
        Executable(func=mul, args=(5, 2)),
    ]

    executor = PoolExecutor(executables, use_multi_threading)

    results = executor.execute()

    if unwrap_results:
        results = [result.unwrap_or_return() for result in results]

    assert results == expected_result


@pytest.mark.unit
@pytest.mark.parametrize("use_multi_threading", [True, False])
def test_pool_executor_should_fail_when_executable_returns_a_failure(
    use_multi_threading,
):
    def sum(param_1, param_2) -> Result[int, Error]:
        return isFailure

    def mul(param_1, param_2) -> Result[int, Error]:
        return Success(param_1 * param_2)

    executables = [Executable(func=sum, args=(1, 2)), Executable(func=mul, args=(1, 2))]

    executor = PoolExecutor(executables, use_multi_threading)

    results = executor.execute()

    assert results[0].is_failure
    assert results[1].is_success
