from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from deprecation import deprecated

from petisco import __version__
from petisco.base.domain.message.message import Message

TypeMessage = TypeVar("TypeMessage", bound=Message)


class MessageBus(ABC, Generic[TypeMessage]):
    """
    A base class to implement an infrastructure-based bus to publish or dispatch messages.
    """

    @classmethod
    def __repr__(cls) -> str:
        return cls.__name__

    @classmethod
    def info(cls) -> dict[str, str]:
        return {"name": cls.__name__}

    def _set_additional_meta(self, meta: dict[str, Any]) -> None:
        self.additional_meta = meta

    def with_meta(self, meta: dict[str, Any]) -> MessageBus[Message]:
        if not isinstance(meta, Dict):
            raise TypeError("MessageBus.with_meta() expect a dict")
        message_bus = copy.copy(self)
        message_bus._set_additional_meta(meta)
        return message_bus  # type: ignore

    def get_configured_meta(self) -> dict[str, Any]:
        configured_meta: dict[str, Any] = {}
        if hasattr(self, "additional_meta"):
            configured_meta = {**configured_meta, **self.additional_meta}
        return configured_meta

    @abstractmethod
    def publish(self, message: TypeMessage | list[TypeMessage]) -> None:
        """
        Publish a message or a list of messages
        """
        raise NotImplementedError

    def _check_input(
        self, message: TypeMessage | list[TypeMessage]
    ) -> list[TypeMessage]:  # noqa
        if isinstance(message, list):
            messages = message
        else:
            messages = [message]
        return messages

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def _check_is_message(self, message: TypeMessage) -> None:
        if not message or not issubclass(message.__class__, Message):
            raise TypeError("MessageBus only publishes Message objects")

    @deprecated(
        deprecated_in="1.14.0",
        removed_in="2.0.0",
        current_version=__version__,
        details="Use publish function instead",
    )
    def publish_list(self, messages: list[TypeMessage]) -> None:
        for message in messages:
            self.publish(message)
