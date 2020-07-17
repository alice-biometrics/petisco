from meiga import Error


class CriticalError(Error):
    def __init__(self, exception: Exception, executor=None, traceback=None):
        self.message = f"{exception.__class__.__name__}: {str(exception)}"
        self.exception = exception
        self.executor = executor
        self.traceback = traceback

    def __repr__(self):
        executor_str = f" ({self.executor})" if self.executor else ""
        traceback_str = f"\n{self.traceback}" if self.traceback else ""
        return (
            f"{self.__class__.__name__}{executor_str}: {self.message}.{traceback_str}"
        )
