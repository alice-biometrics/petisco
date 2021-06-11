from typing import Optional, List, Dict

from pydantic.main import BaseModel

from petisco.legacy.domain.aggregate_roots.info_id import InfoId


class NotifierMessage(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    info_petisco: Optional[Dict] = None
    info_id: Optional[InfoId] = None
    files: Optional[List[Dict]] = None
