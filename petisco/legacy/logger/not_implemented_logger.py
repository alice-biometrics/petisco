from petisco.legacy.logger.interface_logger import ILogger
from petisco.legacy.logger.log_message import LogMessage


class NotImplementedLogger(ILogger):
    def log(self, logging_level, log_message: LogMessage):
        pass
