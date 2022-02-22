from petisco.base.domain.errors.unknown_error import UnknownError


class NotifierExceptionMessage:
    title: str
    executor: str
    exception: Exception
    traceback: str
    filename: str = None
    lineno: str = None
    input_parameters: dict = None
    meta: dict = None

    def __init__(
        self,
        title: str,
        executor: str,
        exception: Exception,
        traceback: str,
        filename: str = None,
        lineno: str = None,
        input_parameters: dict = None,
        meta: dict = None,
    ):
        self.title = title
        self.executor = executor
        self.exception = exception
        self.traceback = traceback
        self.filename = filename
        self.lineno = lineno
        self.input_parameters = input_parameters
        self.meta = meta

    def update_meta(self, meta: dict):
        self.meta = {**self.meta, **meta}

    @staticmethod
    def from_unknown_error(unknown_error: UnknownError, title: str):
        return NotifierExceptionMessage(
            title=title,
            executor=unknown_error.executor,
            exception=unknown_error.exception,
            traceback=unknown_error.traceback,
            filename=unknown_error.filename,
            lineno=unknown_error.lineno,
            input_parameters=unknown_error.input_parameters,
            meta=unknown_error.meta,
        )
