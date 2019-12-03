from typing import Any

from petisco.logger.log_message import LogMessage


class LogMessageMother:
    @staticmethod
    def get_controller(
        operation: str = None, correlation_id: str = None, message: str = None
    ) -> LogMessage:
        return LogMessage(
            layer="controller",
            operation=operation,
            correlation_id=correlation_id,
            message=message,
        )

    @staticmethod
    def get_use_case(
        operation: str = None, correlation_id: str = None, message: Any = None
    ) -> LogMessage:
        return LogMessage(
            layer="use_case",
            operation=operation,
            correlation_id=correlation_id,
            message=message,
        )

    @staticmethod
    def get_command(
        operation: str = None, correlation_id: str = None, message: str = None
    ) -> LogMessage:
        return LogMessage(
            layer="command",
            operation=operation,
            correlation_id=correlation_id,
            message=message,
        )
