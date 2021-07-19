from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_bus import MessageBus


class NotImplementedMessageBus(MessageBus):
    def publish(self, message: Message):
        self._check_is_message(message)
        meta = self.get_configured_meta()
        _ = message.update_meta(meta)

    def retry_publish_only_on_store_queue(self, message: Message):
        self._check_is_message(message)
        meta = self.get_configured_meta()
        _ = message.update_meta(meta)

    def close(self):
        pass
