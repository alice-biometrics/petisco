import sys

from petisco.extra.threading.executable import Executable, ExecutableError
from petisco.extra.threading.multiprocessing_pool_executor import MultiprocessingPoolExecutor, PoolExecutor

threading = [
    "MultiprocessingPoolExecutor",
    "PoolExecutor",
    "Executable",
    "ExecutableError",
]

if sys.version_info >= (3, 10):
    from petisco.extra.threading.concurrent_futures_pool_executor import ConcurrentFuturesPoolExecutor

    threading += ["ConcurrentFuturesPoolExecutor"]


__all__ = threading
