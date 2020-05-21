from typing import Any, Dict, List

from dataclasses import dataclass

from petisco.domain.aggregate_roots.info_id import InfoId


@dataclass
class NotifierMessage:
    message: str = None
