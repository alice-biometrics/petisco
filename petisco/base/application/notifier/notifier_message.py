from typing import Dict, List, Optional

from pydantic.main import BaseModel


class NotifierMessage(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    meta: Optional[Dict] = None
    files: Optional[List[Dict]] = None
    # info_id: Optional[InfoId] = None
