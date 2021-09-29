import sys
import traceback
from typing import Any, Dict, List, Optional

from meiga import Error


class UnknownError(Error):
    def __init__(
        self,
        exception: Exception,
        input_parameters=None,
        executor=None,
        traceback=None,
        filename=None,
        lineno=None,
        filter_parameters: List[str] = None,
        meta: Dict = None,
    ):
        self.message = f"{exception.__class__.__name__}: {str(exception)}"
        self.input_parameters = self._sanitize_input_params(input_parameters)
        self._filter_input_parameters(filter_parameters)
        self.exception = exception
        self.executor = executor
        self.traceback = traceback
        self.filename = filename
        self.lineno = lineno
        self.meta = meta if meta else {}

    def _sanitize_input_params(self, input_parameters):
        if isinstance(input_parameters, tuple):
            return {
                f"param_{i + 1}": param if not isinstance(param, bytes) else "bytes"
                for i, param in enumerate(input_parameters)
            }
        elif isinstance(input_parameters, dict):
            return {
                k: v if not isinstance(v, bytes) else "bytes"
                for k, v in input_parameters.items()
            }
        else:
            return None

    def _filter_input_parameters(self, filter_parameters: List[str] = None):
        if filter_parameters:
            self.input_parameters = {
                k: v
                for k, v in self.input_parameters.items()
                if k not in filter_parameters
            }

    def __repr__(self):
        executor_str = f" ({self.executor})" if self.executor else ""
        traceback_str = f"\n{self.traceback}" if self.traceback else ""
        input_parameters_str = (
            f"\nInput Parameters: {str(self.input_parameters)}"
            if self.input_parameters
            else ""
        )
        filename_str = f"\n{self.filename}" if self.filename else ""
        lineno_str = f"\n{self.lineno}" if self.lineno else ""
        return f"{self.__class__.__name__}{executor_str}: {self.message}.{traceback_str}.{input_parameters_str}{filename_str}{lineno_str}"

    @classmethod
    def from_exception(
        cls,
        exception: Exception,
        arguments: Any,
        class_name: Optional[str] = None,
    ):
        _, _, tb = sys.exc_info()
        tb = traceback.extract_tb(tb)[-1]
        filename = tb.filename if tb and hasattr(tb, "filename") else None
        lineno = tb.lineno if tb and hasattr(tb, "lineno") else None

        unknown_error = cls(
            exception=exception,
            input_parameters=arguments,
            executor=class_name,
            traceback=traceback.format_exc(),
            filename=filename,
            lineno=lineno,
        )
        return unknown_error
