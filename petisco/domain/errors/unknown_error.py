from petisco.domain.errors.critical_error import CriticalError


class UnknownError(CriticalError):
    def __init__(self, exception: Exception, executor=None, traceback=None):
        self.message = f"{exception.__class__.__name__}: {str(exception)}"
        self.exception = exception
        self.executor = executor
        self.traceback = traceback

    def __repr__(self):

        return f"{self.__class__.__name__} ({self.executor}): {self.message}.\n{self.traceback}"


# 'message': "Result[status: failure | value: UnknownError: AttributeError: 'NoneType' object has no attribute 'get'] -> AttributeError: 'NoneType' object has no attribute 'get'"
