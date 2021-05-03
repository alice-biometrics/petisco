from multiprocessing.pool import ThreadPool
from typing import List, Tuple, Callable


class Executable:
    def __init__(self, func: Callable, args: Tuple):
        self.func = func
        self.args = args


class PoolExecutor:
    def __init__(self, executables: List[Executable], use_multi_threading: bool = True):
        self.executables = executables
        self.use_multi_threading = use_multi_threading

    def execute(self) -> List:
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

    def _coroutine(self, executable: Executable):
        return executable.func(*executable.args)

    def clear(self):
        del self.executables
        self.executables = []
