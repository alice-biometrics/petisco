from typing import Any

from petisco.base.domain.message.legacy.use_legacy_implementation import (
    USE_LEGACY_IMPLEMENTATION,
)
from petisco.base.domain.message.message import Message


class DomainEvent(Message):
    def model_post_init(self, __context: Any) -> None:
        self._message_type = "domain_event"
        super().model_post_init(__context)


if USE_LEGACY_IMPLEMENTATION is True:
    from petisco.base.domain.message.legacy.legacy_domain_event import (  # noqa
        LegacyDomainEvent,
    )

    DomainEvent = LegacyDomainEvent  # noqa
