from typing import Any

from petisco.base.domain.message.message import Message


class Command(Message):
    def model_post_init(self, __context: Any) -> None:
        self._message_type = "command"
        super().model_post_init(__context)
