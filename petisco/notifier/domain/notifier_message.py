from abc import abstractmethod
from typing import Optional, List, Dict

from dataclasses import dataclass

from petisco.domain.aggregate_roots.info_id import InfoId


@dataclass
class NotifierMessage:
    message: str = None
    info_petisco: Optional[Dict] = None
    info_id: Optional[InfoId] = None
    files: Optional[List[Dict]] = None

    @abstractmethod
    def __str__(self) -> str:
        return self.message
