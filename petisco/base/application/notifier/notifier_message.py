from typing import Dict, List, Optional

from pydantic.main import BaseModel


class NotifierMessage(BaseModel):
    title: str
    message: Optional[str] = None
    meta: Optional[Dict] = None
    files: Optional[List[Dict]] = None
    link: Optional[Dict[str, str]] = None
    # info_id: Optional[InfoId] = None
