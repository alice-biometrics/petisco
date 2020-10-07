from typing import Any

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.logger.log_message import LogMessage


class LogMessageMother:
    @staticmethod
    def get_controller(
        operation: str = None, info_id: InfoId = None, message: str = None
    ) -> LogMessage:
        return LogMessage(
            layer="controller",
            operation=operation,
            info_id=info_id,
            data={"message": message},
        )

    @staticmethod
    def get_use_case(
        operation: str = None, info_id: InfoId = None, message: Any = None
    ) -> LogMessage:
        return LogMessage(
            layer="use_case",
            operation=operation,
            info_id=info_id,
            data={"message": message},
        )

    @staticmethod
    def get_command(
        operation: str = None, info_id: InfoId = None, message: str = None
    ) -> LogMessage:
        return LogMessage(
            layer="command",
            operation=operation,
            info_id=info_id,
            data={"message": message},
        )

    @staticmethod
    def get_subscriber(operation: str = None, message: str = None) -> LogMessage:
        return LogMessage(
            layer="subscriber", operation=operation, data={"message": message}
        )

    @staticmethod
    def get_event_handler(operation: str = None, message: str = None) -> LogMessage:
        return LogMessage(
            layer="event_handler", operation=operation, data={"message": message}
        )
