from meiga import Error


class UnknownError(Error):
    def __init__(self, exception: Exception, executor=None, traceback=None):
        self.message = f"{exception.__class__.__name__}: {str(exception)}"
        self.exception = exception
        self.executor = executor
        self.traceback = traceback
