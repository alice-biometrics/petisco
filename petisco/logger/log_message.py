from typing import Any

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class LogMessage:
    layer: str = None
    operation: str = None
    correlation_id: str = None
    message: Any = None
