from typing import Any, Callable, Tuple, Union

from petisco import CriticalError


class Executable:
    def __init__(
        self,
        func: Callable[[Any], Any],
        args: Tuple[Any],
        name: Union[str, None] = None,
        prioritized: bool = False,
    ) -> None:
        """
        func: Callable to run the action
        args: Argument to pass to Callable
        name: Optional name to identify the executable
        prioritized: Option to define prioritization for executables (Classes as PoolExecutor use them to order tasks)
        """
        self.func = func
        self.args = args
        self.name = self.func.__qualname__ if name is None else name
        self.prioritized = prioritized

    def coroutine(self) -> Any:
        return self.func(*self.args)


class ExecutableError(CriticalError):
    pass
