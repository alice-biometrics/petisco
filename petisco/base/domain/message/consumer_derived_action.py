from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ConsumerDerivedAction(BaseModel):
    action: str | None = None
    exchange_name: str | None = None
    routing_key: str | None = None
    headers: dict[str, Any] | None = None
