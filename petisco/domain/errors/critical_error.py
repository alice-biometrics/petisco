from meiga import Error


class CriticalError(Error):
    def __init__(
        self, exception: Exception, input_params=None, executor=None, traceback=None
    ):
        self.message = f"{exception.__class__.__name__}: {str(exception)}"
        self.input_params = self._sanitize_input_params(input_params)
        self.exception = exception
        self.executor = executor
        self.traceback = traceback

    def _sanitize_input_params(self, input_params):
        if isinstance(input_params, tuple):
            return {
                f"param_{i}": param if not isinstance(param, bytes) else "bytest"
                for i, param in enumerate(input_params)
            }
        elif isinstance(input_params, dict):
            return {
                k: v if not isinstance(v, bytes) else "bytest"
                for k, v in input_params.items()
            }
        else:
            return None

    def __repr__(self):
        executor_str = f" ({self.executor})" if self.executor else ""
        traceback_str = f"\n{self.traceback}" if self.traceback else ""
        input_params_str = (
            f"\nInput Parameters: {str(self.input_params)}" if self.input_params else ""
        )

        return f"{self.__class__.__name__}{executor_str}: {self.message}.{traceback_str}.{input_params_str}"
