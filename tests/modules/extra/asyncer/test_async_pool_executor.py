from typing import List

import anyio
import pytest

from petisco.extra.asyncer import is_asyncer_available
from petisco.extra.threading import Executable


async def executable_func(value: str) -> str:
    await anyio.sleep(1)
    return value


@pytest.mark.integration
@pytest.mark.skipif(
    not is_asyncer_available(), reason="Only test it when asyncer is available"
)
class TestAsyncPoolExecutor:
    executables: List[Executable]

    def setup_method(self):
        self.executables = [
            Executable(executable_func, ("executable 1",)),
            Executable(executable_func, ("executable 2",)),
            Executable(executable_func, ("executable 3",)),
        ]

    @pytest.mark.asyncio
    async def should_execute_successfully(self):
        from petisco.extra.asyncer import AsyncPoolExecutor

        pool_executor = AsyncPoolExecutor(self.executables)
        func_results = await pool_executor.execute()
        assert func_results == ["executable 1", "executable 2", "executable 3"]
