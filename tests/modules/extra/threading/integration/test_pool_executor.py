import pytest

from petisco.extra.threading import Executable, PoolExecutor


def executable_func(value: str) -> str:
    return value


@pytest.mark.integration
class TestPoolExecutor:
    executables: list[Executable]

    def setup_method(self):
        self.executables = [
            Executable(executable_func, ("executable 1",)),
            Executable(executable_func, ("executable 2",)),
            Executable(executable_func, ("executable 3",)),
        ]

    @pytest.mark.parametrize("use_multi_threading", [True, False])
    def should_execute_successfully(self, use_multi_threading: bool):
        pool_executor = PoolExecutor(self.executables, use_multi_threading)
        func_results = pool_executor.execute()

        assert func_results == ["executable 1", "executable 2", "executable 3"]
