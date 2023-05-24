from typing import Any, Dict, Optional

from pydantic import BaseModel


class ConsumerDerivedAction(BaseModel):
    action: Optional[str] = None
    exchange_name: Optional[str] = None
    routing_key: Optional[str] = None
    headers: Optional[Dict[str, Any]] = None
