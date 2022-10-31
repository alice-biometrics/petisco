from multiprocessing.pool import ThreadPool
from typing import Any, Callable, List, Tuple


class Executable:
    def __init__(self, func: Callable[[Any], Any], args: Tuple[Any]) -> None:
        self.func = func
        self.args = args


class PoolExecutor:
    def __init__(
        self, executables: List[Executable], use_multi_threading: bool = True
    ) -> None:
        self.executables = executables
        self.use_multi_threading = use_multi_threading

    def execute(self) -> List[Any]:
        if len(self.executables) < 1:
            return []

        func_results = []
        if self.use_multi_threading:
            pool = ThreadPool(len(self.executables))
            func_results = pool.map(self._coroutine, self.executables)
            pool.close()
            pool.join()
            pool.terminate()
        else:
            for executable in self.executables:
                func_results.append(self._coroutine(executable))
        return func_results

    def _coroutine(self, executable: Executable) -> Any:
        return executable.func(*executable.args)

    def clear(self) -> None:
        del self.executables
        self.executables = []
