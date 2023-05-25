from __future__ import annotations

from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_bus import MessageBus


class NotImplementedMessageBus(MessageBus[Message]):
    def publish(self, message: Message) -> None:
        self._check_is_message(message)
        meta = self.get_configured_meta()
        _ = message.update_meta(meta)

    def close(self) -> None:
        pass
