from typing import Any, Callable, List, Tuple

import asyncer


class Executable:
    def __init__(self, func: Callable[[Any], Any], args: Tuple[Any]) -> None:
        self.func = func
        self.args = args


class AsyncPoolExecutor:
    def __init__(self, executables: List[Executable]) -> None:
        self.executables = executables

    async def execute(self) -> List[Any]:
        if len(self.executables) < 1:
            return []

        func_results = []

        async with asyncer.create_task_group() as task_group:
            for executable in self.executables:
                result = task_group.soonify(self._coroutine)(executable)
                func_results.append(result)

        func_results = [result.value for result in func_results]
        return func_results

    def _coroutine(self, executable: Executable) -> Any:
        return executable.func(*executable.args)

    def clear(self) -> None:
        del self.executables
        self.executables = []
