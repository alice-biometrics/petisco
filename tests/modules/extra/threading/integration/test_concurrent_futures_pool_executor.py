from __future__ import annotations

import sys

import pytest

from petisco.extra.threading import Executable

if sys.version_info < (3, 10):
    ConcurrentFuturesPoolExecutor = None  # Not available
else:
    from petisco.extra.threading import ConcurrentFuturesPoolExecutor


def executable_func(value: str) -> str:
    return value


@pytest.mark.integration
@pytest.mark.skipif(sys.version_info < (3, 10), reason="Only available in Python 3.10+")
class TestConcurrentFuturesPoolExecutor:
    executables: list[Executable]

    def setup_method(self):
        self.executables = [
            Executable(executable_func, ("executable 1",)),
            Executable(executable_func, ("executable 2",)),
            Executable(executable_func, ("executable 3",)),
        ]

    @pytest.mark.parametrize("use_multi_threading", [True, False])
    def should_execute_successfully(self, use_multi_threading: bool):
        pool_executor = ConcurrentFuturesPoolExecutor(self.executables, use_multi_threading)
        func_results = pool_executor.execute()
        assert sorted(func_results) == ["executable 1", "executable 2", "executable 3"]
