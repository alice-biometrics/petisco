import json
from abc import abstractmethod
from typing import Optional, List, Dict

from dataclasses import dataclass

from petisco.domain.aggregate_roots.info_id import InfoId


@dataclass
class NotifierMessage:
    title: str = None
    message: str = None
    info_petisco: Optional[Dict] = None
    info_id: Optional[InfoId] = None
    files: Optional[List[Dict]] = None

    @abstractmethod
    def __str__(self) -> str:
        return f"Title: {self.title}\nMessage: {self.message}\nPetisco info: {json.dumps(self.info_petisco)}\nInfo Id: {json.dumps(self.info_id)}"
