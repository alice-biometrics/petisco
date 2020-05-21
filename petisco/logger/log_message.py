from typing import Any, Dict

from dataclasses import dataclass

from petisco.domain.aggregate_roots.info_id import InfoId


@dataclass
class LogMessage:
    layer: str = None
    operation: str = None
    info_id: InfoId = None
    data: Dict[str, Any] = None

    def to_dict(self):
        dict_log_message = {"data": self.data, "meta": {}}
        if self.layer:
            dict_log_message["meta"]["layer"] = self.layer
        if self.operation:
            dict_log_message["meta"]["operation"] = self.operation
        if self.info_id:
            info_id: dict = self.info_id.to_dict()
            dict_log_message["meta"]["info_id"] = info_id

        return dict_log_message

    def set_message(self, message: Any):
        self.data = {"message": message}
        return self
