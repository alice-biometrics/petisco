from petisco.logger.log_message import LogMessage
from petisco.logger.interface_logger import ILogger


class NotImplementedLogger(ILogger):
    def log(self, logging_level, log_message: LogMessage):
        pass
