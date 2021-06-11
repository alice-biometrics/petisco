import copy
from typing import Dict, List
from abc import abstractmethod, ABC

from petisco.legacy.domain.aggregate_roots.info_id import InfoId
from petisco.base.domain.message.message import Message


class MessageBus(ABC):
    @classmethod
    def __repr__(cls):
        return cls.__name__

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    def _set_info_id(self, info_id: InfoId):
        self.info_id = info_id

    def _set_additional_meta(self, meta: Dict):
        self.additional_meta = meta

    def with_info_id(self, info_id: InfoId):
        event_bus = copy.copy(self)
        event_bus._set_info_id(info_id)
        return event_bus

    def with_meta(self, meta: Dict, info_id: InfoId = None):
        if not isinstance(meta, Dict):
            raise TypeError("MessageBus.update_meta() expect a dict")
        event_bus = copy.copy(self)
        event_bus._set_additional_meta(meta)
        if info_id:
            event_bus._set_info_id(info_id)
        return event_bus

    def get_configured_meta(self) -> Dict:
        configured_meta = {}
        if hasattr(self, "info_id"):
            configured_meta = {**configured_meta, **self.info_id.to_dict()}
        if hasattr(self, "additional_meta"):
            configured_meta = {**configured_meta, **self.additional_meta}
        return configured_meta

    @abstractmethod
    def publish(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    def retry_publish_only_on_store_queue(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def _check_is_message(self, message: Message):
        if not message or not issubclass(message.__class__, Message):
            raise TypeError("MessageBus only publishes Message objects")

    def publish_list(self, messages: List[Message]):
        for message in messages:
            self.publish(message)

    def retry_publish_list_only_on_store_queue(self, messages: List[Message]):
        for message in messages:
            self.retry_publish_only_on_store_queue(message)
