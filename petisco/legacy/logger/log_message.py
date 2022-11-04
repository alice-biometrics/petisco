from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class LogMessage:
    layer: str = None
    operation: str = None
    data: Dict[str, Any] = None

    def to_dict(self):
        dict_log_message = {"data": self.data, "meta": {}}
        if self.layer:
            dict_log_message["meta"]["layer"] = self.layer
        if self.operation:
            dict_log_message["meta"]["operation"] = self.operation

        return dict_log_message

    def set_message(self, message: Any):
        self.data = {"message": message}
        return self
