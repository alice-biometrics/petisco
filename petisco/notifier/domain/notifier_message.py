from typing import Any, Dict

from dataclasses import dataclass

from petisco.domain.aggregate_roots.info_id import InfoId


@dataclass
class NotifierMessage:
    layer: str = None
    operation: str = None
    info_id: InfoId = None
    data: Dict[str, Any] = None
