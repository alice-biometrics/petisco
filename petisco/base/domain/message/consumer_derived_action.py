from typing import Dict, Optional

from pydantic.main import BaseModel


class ConsumerDerivedAction(BaseModel):
    action: Optional[str] = None
    exchange_name: Optional[str] = None
    routing_key: Optional[str] = None
    headers: Optional[Dict] = None
