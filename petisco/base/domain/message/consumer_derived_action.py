from typing import Any, Optional

from pydantic import BaseModel


class ConsumerDerivedAction(BaseModel):
    action: Optional[str] = None
    exchange_name: Optional[str] = None
    routing_key: Optional[str] = None
    headers: Optional[dict[str, Any]] = None
