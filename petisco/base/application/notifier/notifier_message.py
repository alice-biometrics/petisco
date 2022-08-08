from typing import Any, Dict, List, Optional

from pydantic.main import BaseModel


class NotifierMessage(BaseModel):
    title: str
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    files: Optional[List[Dict[str, Any]]] = None
    link: Optional[Dict[str, str]] = None
    # info_id: Optional[InfoId] = None
