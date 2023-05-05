from petisco.extra.logger.log_message import LogMessage
from petisco.extra.logger.logger import Logger


class NotImplementedLogger(Logger):
    def log(self, logging_level, log_message: LogMessage):
        pass
