from typing import Any

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from petisco.domain.aggregate_roots.info_id import InfoId


@dataclass_json
@dataclass
class LogMessage:
    layer: str = None
    operation: str = None
    info_id: InfoId = None
    message: Any = None
