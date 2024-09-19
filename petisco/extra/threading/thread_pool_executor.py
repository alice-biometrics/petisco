from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from loguru import logger

from petisco.extra.threading.executable import Executable, ExecutableError


class ConcurrentFuturesPoolExecutor:
    """
    petisco pool executor based on from concurrent.futures import ThreadPoolExecutor
    """

    def __init__(self, executables: list[Executable], use_multi_threading: bool = True) -> None:
        self.executables = executables
        self.use_multi_threading = use_multi_threading

    def execute(self) -> list[Any]:
        if len(self.executables) < 1:
            return []

        func_results = []
        if self.use_multi_threading:
            with ThreadPoolExecutor(len(self.executables)) as executor:
                sorted_executables = sorted(
                    self.executables,
                    key=lambda executable: executable.prioritized,
                    reverse=True,
                )

                future_to_executable = {
                    executor.submit(executable.coroutine): executable.name
                    for executable in sorted_executables
                }

                for future in as_completed(future_to_executable):
                    executable_name = future_to_executable[future]
                    try:
                        result = future.result()
                        func_results.append(result)
                    except StopIteration:
                        break
                    except Exception as exc:
                        logger.opt(exception=exc).error(f"PoolExecutor error: {executable_name}")
                        raise ExecutableError(
                            additional_info={
                                "error": str(exc),
                                "executable_name": executable_name,
                            }
                        ) from exc

        else:
            for executable in self.executables:
                func_results.append(executable.coroutine())
        return func_results

    def clear(self) -> None:
        del self.executables
        self.executables = []
